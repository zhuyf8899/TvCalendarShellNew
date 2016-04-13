#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#tools.py:用于在线维护或测试readHtml.py的部分功能的小工具集
import urllib  
import urllib2
import cookielib
import re
import string
import json
import sys
import math
from bs4 import BeautifulSoup
from database import Database
from log import Log

class Tools(object):
    """docstring for Tools"""
    def __init__(self, config):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.config = config
        self.log = Log()
        #剧名的字母顺序表
        self.AllShowsList = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #月份换算表
        self.month = {
            'Jan' : '01',
            'Feb' : '02',
            'Mar' : '03',
            'Apr' : '04',
            'May' : '05',
            'Jun' : '06',
            'Jul' : '07',
            'Aug' : '08',
            'Sep' : '09',
            'Oct' : '10',
            'Nov' : '11',
            'Dec' : '12'
        }

    def flush_one_page(self,character):
        #刷新某一页所有剧的方法，character是一个大写字母
        try:
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            #urlX = 'http://www.pogdesign.co.uk/cat/all-shows/0'
            req = urllib2.Request(
                #从config中取出Allshows的所需要的url，加上上面那个数组所对应的头字母
                url = self.config.urlAllShows+str(character)
            )
            htmlData = ""
            #获取网页原始数据
            htmlData = opener.open(req).read()
        except Exception, connErr:
            self.log.takeLog('ERROR','Connection Error:' + str(connErr))
        if htmlData:
            try:
                for OneBox in BeautifulSoup(htmlData).findAll('div', attrs={'class' : 'contbox prembox removed'}) : #用bs取到所有的小box，每个box是一个剧名
                    showName = BeautifulSoup(str(OneBox)).h2.get_text()
                    showName = showName.replace("'","\\'")
                    imageURL = str(BeautifulSoup(str(OneBox)).a['style'])                                           #此处获取到的是图片URL的一段style的js连接，需要精加工
                    statusStringArray = BeautifulSoup(str(OneBox)).find('span',attrs={'class':'hil selby'})         #此处是要获得剧状态的span标签
                    statusString = str(statusStringArray.get_text()).split('|')                                     #此处是要获得span标签中的内容，之后把|左半拉的内容取出来，但是由于含有空格需要精加工
                    #print(statusString)#标签从这里入手
                    #这个是标签
                    tag = statusString[1][1:-1]
                    tag = tag.replace('Â ',' ')#过滤空格
                    tag = tag.replace("\'","\\'")
                    #exit(1)                                
                    aShow = {
                        's_name' : showName,
                        's_sibox_image' : imageURL[22:-2],
                        'link' : BeautifulSoup(str(OneBox)).a['href'],
                        'status' : statusString[0][1:-1]
                    }
                    #print(aShow)
                    if aShow['s_name'] == '' or aShow['link'] == '' or aShow['status'] == '' :
                        self.log.takeLog('WARNING','''allShowsWork function cannot collect data correctly, the vars are like below:\n s_name=%s,s_sibox_image=%s,link=%s,status=%s'''%(aShow['s_name'],aShow['s_sibox_image'],aShow['link'],aShow['status']))
                    db = Database(self.log,self.config)
                    Id = db.insertShowFirstTime(aShow)
                    if len(tag) != 0:
                        db.insertTag(Id,tag);
            except Exception, syntaxErr:
                self.log.takeLog('ERROR','Syntax Tree Error:' + str(syntaxErr))
            return

    def workWithOneShowsEp(self,s_id):
        #用来仅仅更新一部剧的所有季和集的方法
        db = Database(self.log,self.config)
        urlTarget = self.config.url+db.getOneLinkBySid(s_id)
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        req = urllib2.Request(
            url = urlTarget
        )
        htmlData = ""
        htmlData = opener.open(req).read()
        if htmlData:
            bsContent = BeautifulSoup(htmlData)
            bsLists = bsContent.findAll('div',attrs = {'class':'box930 lists'})
            if len(bsLists) >= 2:
                    pass
            elif len(bsLists) == 1:
                bsLists.append(BeautifulSoup("<html><body><div>none</div></body></html>").find('div'))
            else:
                for i in xrange(1,3):
                    bsLists.append(BeautifulSoup("<html><body><div>none</div></body></html>").find('div'))
            for bsToBeAired in bsLists[0].findAll('div'):  #遍历查找即将播放的集,如果没有则不执行该循环
                seEpInfo = bsToBeAired.find('span',attrs = {'class' : 'epuntil'}).get_text()    #季与集的信息
                season = re.search('S\d*',seEpInfo).group()     #首先用正则取出季，形如S02
                if season[1] == '0':                            #之后将S和多余的0都去掉
                    season = season[2:]
                else:
                    season = season[1:]
                episode = re.search('E\d*',seEpInfo).group()    #同理对付集数
                if episode[1] == '0':
                    episode = episode[2:]
                else:
                    episode = episode[1:]
                dateInfo = bsToBeAired.find('span',attrs = {'class' : 'epdate'}).get_text()     #接下来处理日期，比较折腾
                year = re.search("'.*$",dateInfo).group()                                       #首先摘出形如‘16的表示年份的字串，并取出前面的’
                year = year[1:]
                month = re.search(' \w{3} ',dateInfo).group()                                   #接着取出三个代表月份的字母，形如Feb，并删除前后空格
                month = month[1:-1]
                day = re.search('^\d*',dateInfo).group()                                        #再之后取出日期，如果日期是个位数前面补零以保证yyyy-mm-dd的格式
                if len(day) < 2:
                    day = '0'+day
                time = bsToBeAired.find('span',attrs = {'class' : 'eptime'}).get_text()         #取出日期后开始调整时间，利用类似的方法获取小时和分钟
                hour = re.search('\d{1,2}:',time).group()
                hour = hour[:-1]
                hour = string.atoi(hour)
                minute = re.search(':\d{2}[a|p]m',time).group() 
                #注意调整am和pm的时间差，另外需要注意的是这里的时间都是标准UTC时间，天朝使用需要+8
                if (minute[-2] == 'p') and (hour != 12):
                    hour += 12
                minute = minute[1:-2]
                    
                dateFormat = year + '-' +  self.month[month] + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) +':00'
                name =  bsToBeAired.find('span',attrs = {'class' : 'epname'}).get_text()
                name = name[1:]
                name = name.replace("'","\\'")
                
                episodeInfoToBeAired = {
                    's_id' : s_id,
                    'se_id' : season,
                    'e_num' : episode,
                    'e_name' : name,
                    'e_status' : u"即将播出",
                    'e_description' : '',
                    'e_time' : dateFormat

                }
                print(episodeInfoToBeAired)
                db.insertEpisode(episodeInfoToBeAired)

            for bsHaveAired in bsLists[1].findAll('div',attrs = {'class':'prevlist'}):
                seEpInfo = bsHaveAired.find('span',attrs = {'class' : 'epuntil'}).get_text()
                season = re.search('S\d*',seEpInfo).group()
                if season[1] == '0':
                    season = season[2:]
                else:
                    season = season[1:]
                episode = re.search('E\d*',seEpInfo).group()
                if episode[1] == '0':
                    episode = episode[2:]
                else:
                    episode = episode[1:]
                dateInfo = bsHaveAired.find('span',attrs = {'class' : 'epdate'}).get_text()
                year = re.search("'.*$",dateInfo).group()
                year = year[1:]
                year = string.atoi(year)
                if(year >= 60):
                    year = '19' + str(year)
                else:
                    if len(str(year))<2:
                        year = '200' + str(year)
                    else:
                        year = '20' + str(year)

                month = re.search(' \w{3} ',dateInfo).group()
                month = month[1:-1]
                day = re.search('^\d*',dateInfo).group()
                if len(day) < 2:
                    day = '0'+day
                time = bsHaveAired.find('span',attrs = {'class' : 'eptime'}).get_text()
                hour = re.search('\d{1,2}:',time).group()
                hour = hour[:-1]
                hour = string.atoi(hour)
                minute = re.search(':\d{2}[a|p]m',time).group()
                if (minute[-2] == 'p') and (hour != 12):
                    hour += 12
                minute = minute[1:-2]
                    
                dateFormat = year + '-' +  self.month[month] + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) +':00'
                name =  bsHaveAired.find('span',attrs = {'class' : 'epname'}).get_text()
                name = name[1:]
                name = name.replace("'","\\'")
                
                episodeInfoHaveAired = {
                    's_id' : s_id,
                    'se_id' : season,
                    'e_num' : episode,
                    'e_name' : name,
                    'e_status' : u"已播出",
                    'e_description' : '',
                    'e_time' : dateFormat
                }
                print(episodeInfoHaveAired)
                db.insertEpisode(episodeInfoHaveAired)

