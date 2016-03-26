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
                if (minute[-2] == 'p') and (minute[1:2] != '12'):
                    hour += 12
                minute = minute[1:-2]
                    
                dateFormat = '20' + year + '-' +  self.month[month] + '-' + day + ' ' + str(hour) + ':' + minute +':00'
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
                if (minute[-2] == 'p') and (minute[1:2] != '12'):
                    hour += 12
                minute = minute[1:-2]
                    
                dateFormat = '20' + year + '-' +  self.month[month] + '-' + day + ' ' + str(hour) + ':' + minute +':00'
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

