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
#import MySQLdb
from bs4 import BeautifulSoup
from database import Database
from log import Log

class Tools(object):
    """A class which is very simililar to ReadHtml class. The diffierence is it use step-forward method to handle data mannually"""
    def __init__(self, config):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.config = config
        self.log = Log()
        #剧名的字母顺序表
        self.AllShowsList = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #月份换算表
        #已废弃，处于兼容目的保留
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
            #try:
            for OneBox in BeautifulSoup(htmlData).findAll('div', attrs={'class' : 'contbox prembox removed'}) : #用bs取到所有的小box，每个box是一个剧名
                showName = BeautifulSoup(str(OneBox)).h2.get_text()
                showName = showName.replace("'","\\'")
                imageURL = str(BeautifulSoup(str(OneBox)).a['style'])                                           #此处获取到的是图片URL的一段style的js连接，需要精加工
                statusStringArray = BeautifulSoup(str(OneBox)).find('span',attrs={'class':'hil selby'})         #此处是要获得剧状态的span标签
                
                #edit on 20160520由于原网页出现格式变化，改从注释中提取播放状态，一旦注释消失记得修改此处注释内容
                statusString = str(statusStringArray).split('|')                                     #此处是要获得span标签中的内容，之后把|左半拉的内容取出来，但是由于含有空格需要精加工
                #标签从这里入手
                #print (str(statusStringArray))
                #这个是标签
                tag = statusString[1][4:-8]
                tag = tag.replace('Â ',' ')#过滤空格
                tag = tag.replace("\'","\\'")
                #print(tag)                             
                
                aShow = {
                    's_name' : showName,
                    's_sibox_image' : imageURL[22:-2],
                    'link' : BeautifulSoup(str(OneBox)).a['href'],
                    'status' : statusString[0][29:-1]
                }
                #print(aShow)
                if aShow['s_name'] == '' or aShow['link'] == '' or aShow['status'] == '' :
                #if aShow['s_name'] == '' or aShow['link'] == '' :
                    self.log.takeLog('WARNING','''allShowsWork function cannot collect data correctly, the vars are like below:\n s_name=%s,s_sibox_image=%s,link=%s,status=%s'''%(aShow['s_name'],aShow['s_sibox_image'],aShow['link'],aShow['status']))
                db = Database(self.log,self.config)
                Id = db.insertShowFirstTime(aShow)
                if len(tag) != 0:
                    db.insertTag(Id,tag);
            #except Exception, syntaxErr:
            #    self.log.takeLog('ERROR','Syntax Tree Error:' + str(syntaxErr))
            #    raise syntaxErr
            return

    def updateShowDetail(self,s_id):
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
            pinfo = bsContent.find('p',attrs={'class':'sumtext'}).get_text()  #要取到的剧的介绍
            pinfo = pinfo.replace("'", "\\'")
            DivLarge = bsContent.find('aside',attrs={'class':'quikinfo'})
            DivSmall = DivLarge.findAll('li')
            #处理每周日期
            update_time = DivSmall[0].a.get_text()
            #处理每集长度
            length = DivSmall[1].get_text()
            length = length[17:]
            #查找地区、电视台
            area = DivSmall[3].get_text()
            area = area[10:]
            channel = DivSmall[2].get_text()
            channel = channel[10:]
        
            DetailOfShow = {
                's_id' : s_id,
                's_description' : pinfo,
                'update_time' : update_time,
                'length' : length,
                'area' : area,
                'channel' : channel
            }
            print DetailOfShow
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
            bsLists = bsContent.findAll('li',attrs = {'class':'parent'})
            print ('the len of biLists is '+str(len(bsLists)))
            for oneSeason in bsLists:
                se_id = oneSeason.strong.get_text()
                se_id = re.search('Season\s\d{1,2}',se_id).group()
                se_id = se_id[7:]

                for oneEpisode in oneSeason.findAll('li',attrs = {'class':'ep info  RAWR'}):
                    #集数
                    e_num = oneEpisode.find('span',attrs = {'class':'pnumber'}).get_text()
                    if e_num[0] == '0':
                        e_num = e_num[1:]
                    #集名
                    e_name = oneEpisode.find('a',attrs = {'itemprop':'url'}).get_text()
                    #e_name = MySQLdb.escape_string(e_name)
                    #播放时间

                    time_temp = oneEpisode.find('span',attrs = {'class':'datepub'})
                    e_time = time_temp['content']
                    time_temp = time_temp.get_text()
                    time = time_temp[-7:]

                    hour = re.search('\d{1,2}:',time).group()
                    hour = hour[:-1]
                    hour = string.atoi(hour)
                    minute = re.search(':\d{2}[a|p]m',time).group() 
                    #注意调整am和pm的时间差，另外需要注意的是这里的时间都是标准UTC时间，天朝使用需要+8
                    if (minute[-2] == 'p') and (hour != 12):
                        hour += 12
                    minute = minute[1:-2]

                    if len(str(hour)) < 2:
                        hour = '0' + str(hour)
                    
                    e_time += ' ' + str(hour) + ':' + minute + ':00'

                    status_temp = oneEpisode.find('span',attrs = {'class':'paired'}).get_text()
                    if status_temp == 'AIRED':
                        e_status = u'已播放'
                    else:
                        e_status = u'即将播出'

                    episodeInfoToBeAired = {
                        's_id' : s_id,
                        'se_id' : se_id,
                        'e_num' : e_num,
                        'e_name' : e_name,
                        'e_status' : e_status,
                        'e_description' : '',
                        'e_time' : e_time

                    }
                    print episodeInfoToBeAired
                flag = False
                if flag == False:
                    break

    def test_connection(self):
        #检查连接连通性，如联通则输出页面内容，如不则报失败
        urlTarget = 'http://www.pogdesign.co.uk/cat/'
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        req = urllib2.Request(
            url = urlTarget
        )
        htmlData = ""
        htmlData = opener.open(req).read()
        if htmlData:
            print "OK"
            print htmlData
        else:
            print "Connection Error"
        return