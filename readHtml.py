#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#readHtml.py:网页文档解析器模块
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

class Reader(object):
    """读取HTML的类"""
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
        

    def allShowsWork(self):
        #初步获取show的方法
        for i in xrange(0,len(self.AllShowsList)):  #注意这里是0~len，并不是0~len-1
            try:
                cookie = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                #urlX = 'http://www.pogdesign.co.uk/cat/all-shows/0'
                req = urllib2.Request(
                    #从config中取出Allshows的所需要的url，加上上面那个数组所对应的头字母
                    url = self.config.urlAllShows+self.AllShowsList[i]
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
                        #print(statusString)#以后装标签从这里入手
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
                        db.insertShowFirstTime(aShow)
                except Exception, syntaxErr:
                    self.log.takeLog('ERROR','Syntax Tree Error:' + str(syntaxErr))
        return

    def showDetailsWork(self,urlShow,s_id,firstTime):
        #针对一部剧，完成其show的剩余字段和完成分季和分集的方法
        try:
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            req = urllib2.Request(
                #从config中取出Allshows的所需要的url，加上上面那个数组所对应的头字母
                url = urlShow
            )
            htmlData = ""
            #获取网页原始数据
            htmlData = opener.open(req).read()
        except Exception, connErr:
            self.log.takeLog('ERROR','Connection Error:' + str(connErr))
        
        if htmlData:
            try:
                reString = '</span>\s.*</div>'  #要匹配的正则表达式
                bsContent = BeautifulSoup(htmlData)
                pinfo = bsContent.p.get_text()  #要取到的剧的介绍
                pinfo = pinfo.replace("'", "\\'")
                #print(str(pinfo))
                DivLarge = bsContent.find('div',attrs={'class':'sumdata'})
                DivSmall = DivLarge.findAll('div')
                #处理每周日期
                update_time = re.search(reString,str(DivSmall[1])).group()
                update_time = update_time[8:-6]
                #print(update_time)
                #处理每集长度
                length = re.search(reString,str(DivSmall[2])).group()
                length = length[8:-6]
                #print(length)
                #查找地区、电视台
                area = re.search(reString,str(DivSmall[3])).group()
                area = area[8:-6]
                channel = re.search(reString,str(DivSmall[4])).group()
                channel = channel[8:-6]
            except Exception, ReErr:
                self.log.takeLog('ERROR','Regular Expression Error:' + str(ReErr))
            
            DetailOfShow = {
                's_id' : s_id,
                's_description' : pinfo,
                'update_time' : update_time,
                'length' : length,
                'area' : area,
                'channel' : channel
            }
            if DetailOfShow['s_description'] == '':
                self.log.takeLog('WARNING','''allShowsWork function cannot collect data correctly, the vars are like below:\nDetailOfShow:%s'''%(str(DetailOfShow)))
            try:
                db = Database(self.log,self.config)
                db.updateShowDetail(DetailOfShow)
            except Exception, DBErr:
                self.log.takeLog('ERROR','Database Error:' + str(DBErr))
                self.log.takeLog('DEBUG','problem in showDetailsWork->collecting things in updating shows:')


            #下一步开始整季和集
            try:
                newestSeason = db.selctNewestSeason(s_id) #获取这部剧的最新一季
                bsLists = bsContent.findAll('div',attrs = {'class':'box930 lists'})
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
                    minute = re.search(':\d{2}[a|p]m',time).group()                                 #注意调整am和pm的时间差，另外需要注意的是这里的时间都是标准UTC时间，天朝使用需要+8
                    if (minute[-2] == 'p') and (hour != 12):
                        hour += 12
                    hour = str(hour)
                    if len(hour) == 1:
                        hour = '0' + hour
                    minute = minute[1:-2]
                        
                    dateFormat = '20' + year + '-' +  self.month[month] + '-' + day + ' ' + hour + ':' + minute +':00'
                    name = bsToBeAired.find('span',attrs = {'class' : 'epname'}).get_text()
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
                    #print(episodeInfoToBeAired)
                    #由于即将播出的剧必为最新一季，因此不做检查一定更新
                    db.insertEpisode(episodeInfoToBeAired)

                for bsHaveAired in bsLists[1].findAll('div',attrs = {'class':'prevlist'}):           #接下来是历史播放处理，需要注意的是这里代码与前一段高度吻合，修改时稍加注意
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
                    hour = str(hour)
                    if len(hour) == 1:
                        hour = '0' + hour
                    minute = minute[1:-2]
                    dateFormat = '20' + year + '-' +  self.month[month] + '-' + day + ' ' + hour + ':' + minute +':00'
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
                    #print(episodeInfoHaveAired)
                    if (newestSeason > string.atoi(episodeInfoHaveAired['se_id'])) and (not firstTime):
                        continue
                    else:
                        db.insertEpisode(episodeInfoHaveAired)
            except Exception, DBErr:
                self.log.takeLog('ERROR','Database Error:' + str(DBErr)) 
                self.log.takeLog('DEBUG','problem in showDetailsWork->collecting things in season and eps:')
        return
            

    def finishAllShows(self,firstTime = True):
        #补充show表剩余内容的方法入口，即showDetailsWork的总入口
        try:
            db = Database(self.log,self.config)
            perPage = 100.0
            itemCount = db.selectCountShows()
            pageCount = int(math.ceil(float(itemCount) / perPage))
            for i in xrange(0,pageCount):
                #print(i)
                ids = db.selectSidAndSlinkByLimit(i*100,100)
                for idOne in ids:
                    #print(idOne[0])
                    #print(self.config.url+idOne[1])
                    self.showDetailsWork(self.config.url+idOne[1],idOne[0],firstTime)
        except Exception, DBErr:
            self.log.takeLog('ERROR','Database Error:' + str(DBErr))
            self.log.takeLog('DEBUG','current pageCount:'+str(pageCount))
        return
        

    def testerInEpisode(self,s_id = 1):
        #测试用方法，仅用于调试
        return
            




