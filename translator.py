#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#readHtml.py:翻译模块
import urllib  
import urllib2
import cookielib
import json
from database import Database
from log import Log

class Translator(object):
    """翻译组件"""
    def __init__(self, config):
        super(Translator, self).__init__()
        self.config = config
        self.log = Log()

    def transTag(self):
        #翻译标签的方法
        try:
            db = Database(self.log,self.config)
            tags = db.getAllTagWithoutCN()
            if tags:
                for tagOne in tags:
                    postfix = showOne[1].replace(' ','+')
                    url = self.config.transURL+postfix
                    cookie = cookielib.CookieJar()
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                    req = urllib2.Request(
                        url = url
                    )
                    htmlData = ""
                    #获取网页原始数据
                    htmlData = opener.open(req).read()
                    result = json.loads(htmlData)
                    t_name_cn = ''
                    if result:
                        if 'translation' in result.keys():
                            #print('dic:'+result['translation'][0])
                            t_name_cn = result['translation'][0]
                        elif 'web' in result.keys():
                            #print('web:'+result['web'][0]['value'][0])
                            t_name_cn = result['web'][0]['value'][0]
                        else:
                            continue
                        if t_name_cn:
                            db.updateTagCN(tagOne[0],t_name_cn)
                    else:
                        continue
            else:
                return
            return
        except Exception, TransErr:
            self.log.takeLog('ERROR','Translator Error in tag:' + str(TransErr))

    def transShow(self,alert = 950):
        #翻译剧名的方法，考虑到API限制，每次翻译不超过950次一面被封
        couterAlert = alert
        try:
            db = Database(self.log,self.config)
            shows = db.getAllShowsWithoutCN()
            if shows:
                counter = 0
                for showOne in shows:
                    counter += 1
                    if counter > alert:
                        print('We have reached the alert!')
                        self.log.takeLog('WARNING','Translator API has reached the alert speed. please try it an hour later')
                        break
                    postfix = showOne[1].replace(' ','+')
                    url = self.config.transURL+postfix
                    cookie = cookielib.CookieJar()
                    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                    req = urllib2.Request(
                        url = url
                    )
                    htmlData = ""
                    #获取网页原始数据
                    htmlData = opener.open(req).read()
                    result = json.loads(htmlData)
                    s_name_cn = ''
                    if result:
                        if 'web' in result.keys():
                            #print('web:'+result['web'][0]['value'][0])
                            s_name_cn = result['web'][0]['value'][0]
                        elif 'translation' in result.keys():
                            #print('dic:'+result['translation'][0])
                            s_name_cn = result['translation'][0]
                        else:
                            self.log.takeLog('WARNING','Translator response with empty:' + str(result))
                            print(result)
                            continue
                        if s_name_cn:
                            s_name_cn = s_name_cn.replace("\'","\\'")
                            db.updateShowsCN(showOne[0],s_name_cn)
                    else:
                        continue
            else:
                return
            return
        except Exception, TransErr:
            self.log.takeLog('ERROR','Translator Error in shows:' + str(TransErr))
