#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#数据库模块
import MySQLdb


#conn = MySQLdb.connect(host="localhost",user="root",passwd="123123",db="qiwsirtest",port=3306,charset="utf8")
class Database(object):
    def __init__(self,fileHandler,config):
        self.host = config.dataBaseHost
        self.user = config.dataBaseUser
        self.passwd = config.dataBasePwd
        self.db = config.dataBasedb
        self.hostRes = config.dataBaseHostRes
        self.userRes = config.dataBaseUserRes
        self.passwdRes = config.dataBasePwdRes
        self.dbRes = config.dataBasedbRes
        self.log = fileHandler
    # def __init__(self,config):
    #   self.host = config.dataBaseHost
    #   self.user = config.dataBaseUser
    #   self.passwd = config.dataBasePwd
    #   self.db = config.dataBasedb

    def connect(self,database=''):
        try:
            if database == 'resource':
                conn = MySQLdb.connect(host=self.hostRes,user=self.userRes,passwd=self.passwdRes,db=self.dbRes,charset='utf8')
            else:
                conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset='utf8')
        except Exception, e:
            print(e)
            self.log.takeLog('ERROR','Database Connection Error:'+str(e))
            #self.fileHandler.write(str(e))
            return "connectError"
        return conn
    def insertShowFirstTime(self,obj):#obj中必须有s_name,link,status和s_sibox_image
        try:
            #首先从资源库中找id
            obj['s_name'] = MySQLdb.escape_string(obj['s_name'])
            dbrc = self.connect('resource')
            dbrcHandler = dbrc.cursor()
            sqlGetResource = 'select zmz_resourceid from zmz_resource where resource_en_name = \'%s\' limit 1'%(obj['s_name'])
            dbrcHandler.execute(sqlGetResource)
            resourceResult = dbrcHandler.fetchone()
            #print(resourceResult)
            dbrc.close()
            if resourceResult != None:
                resourceId = resourceResult[0]
            else:
                resourceId = ''
        except Exception,e:
            print(e)
            self.log.takeLog('ERROR','connecting to resource database error:'+str(e)+'\n the sql='+sqlGetResource)
            dbrc.close()
            return "Error"
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sql = 'select s_id,s_name,status,s_sibox_image,r_id from shows where s_name = \'%s\''%(obj['s_name'])
            cursor.execute(sql)
            checker = cursor.fetchone()
            #print(checker)
            if checker:
                if checker[2] == obj['status'] and checker[3] == obj['s_sibox_image'] and checker[4] == resourceId:
                #if checker[3] == obj['s_sibox_image'] and checker[4] == resourceId:
                    dbc.close()
                    print("repeatShow:"+str(obj['s_name']))
                    return checker[0]
                else:
                    if resourceId == '':
                        sql = '''UPDATE `shows` SET  `status` =  \'%s\',`s_sibox_image` =  \'%s\',`link` =  \'%s\' WHERE  `shows`.`s_id` = %s;'''%(obj['status'],obj['s_sibox_image'],obj['link'],checker[0])
                    else:
                        sql = '''UPDATE `shows` SET  `status` =  \'%s\',`s_sibox_image` =  \'%s\',`link` =  \'%s\',`r_id` = \'%s\' WHERE  `shows`.`s_id` = %s;'''%(obj['status'],obj['s_sibox_image'],obj['link'],resourceId,checker[0])
                    #sql = '''UPDATE `shows` SET `s_sibox_image` =  \'%s\',`link` =  \'%s\',`r_id` = \'%s\' WHERE  `shows`.`s_id` = %s;'''%(obj['s_sibox_image'],obj['link'],resourceId,checker[0])
                    cursor.execute(sql)
                    dbc.commit()
                    dbc.close()
                    print('updateShow:'+str(obj['s_name']))
                    return checker[0]
            else:
                if resourceId == '':
                    sql = '''insert into shows(s_name,s_sibox_image,link,status) values(\'%s\',\'%s\',\'%s\',\'%s\')'''%(obj['s_name'],obj['s_sibox_image'],obj['link'],obj['status'])
                else:
                    sql = '''insert into shows(s_name,s_sibox_image,link,r_id,status) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'''%(obj['s_name'],obj['s_sibox_image'],obj['link'],resourceId,obj['status'])
                cursor.execute(sql)
                dbc.commit()
                sqlGetId = '''select s_id from shows where s_name = \'%s\' limit 1'''%(obj['s_name'])
                cursor.execute(sqlGetId)
                Id = cursor.fetchone()
                dbc.close()
                print('insertNewShow:'+str(obj['s_name']))
                return Id[0]
        except Exception,e:
            print(e)
            self.log.takeLog('ERROR','Table shows inserting error:'+str(e)+'\n the sql='+sql)
            dbc.close()
            return "Error"

    def updateShowDetail(self,obj):#obj中必须有s_id,s_description,update_time,area,channel和length
        try:
            obj['s_description'] = MySQLdb.escape_string(obj['s_description'])
            obj['channel'] = MySQLdb.escape_string(obj['channel'])
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlUpdate = '''UPDATE `shows` SET `s_description` = \'%s\',`update_time` = \'%s\',`area` = \'%s\',`length` = \'%s\',`channel` = \'%s\' WHERE `s_id` = \'%s\''''%(obj['s_description'],obj['update_time'],obj['area'],obj['length'],obj['channel'],obj['s_id'])
            cursor.execute(sqlUpdate)
            dbc.commit()
            dbc.close()
            print('update details: '+ str(obj['s_id']))
            return "OK"
        except Exception,e:
            print(e)
            #print(sqlUpdate)
            self.log.takeLog('ERROR','Table show updating error:'+str(e)+'\n the sql='+sqlUpdate)
            dbc.close()
            return "Error"

    def selectCountShows(self):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlCheck = '''select count(s_id) from shows where 1'''
            cursor.execute(sqlCheck)
            counter = cursor.fetchone()
            dbc.close()
            return counter[0]
        except Exception,e:
            print(e)
            self.log.takeLog('ERROR','Table show selecting error:'+ str(e)+'\n the sql='+sqlCheck)
            dbc.close()
            return "Error"
    def selectSidAndSlinkByLimit(self,numLow,numCount):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlCheck = '''select s_id,link from shows where 1 limit %s,%s'''%(numLow,numCount)
            cursor.execute(sqlCheck)
            counter = cursor.fetchall()
            dbc.close()
            return counter
        except Exception,e:
            print(e)
            self.log.takeLog('ERROR','Table show selecting error:'+ str(e)+'\n the sql='+sqlCheck)
            dbc.close()
            return "Error"
    def selctNewestSeason(self,s_id):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlCheck = '''select se_id from episode where s_id = %s order by se_id desc limit 1'''%(s_id)
            cursor.execute(sqlCheck)
            counter = cursor.fetchone()
            dbc.close()
            if counter == None:
                return 0
            else:
                return counter[0]
        except Exception, e:
            self.log.takeLog('ERROR','Table episode selecting error:'+ str(e)+'\n the sql='+sqlCheck)
            print(e)
            dbc.close()
            return "Error"
    def insertEpisode(self,aRecord):
        try:
            aRecord['e_name'] = MySQLdb.escape_string(aRecord['e_name'])
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlCheck = '''select e_id,e_name,e_status,DATE_FORMAT(e_time,'%%Y-%%m-%%d %%T') from episode where s_id = %s AND se_id = %s AND e_num = %s'''%(aRecord['s_id'],aRecord['se_id'],aRecord['e_num'])
            cursor.execute(sqlCheck)
            checker = cursor.fetchone()
            if checker:
                checkerOne =  MySQLdb.escape_string(checker[1])#此处不允许直接修改checker
                #print(checker)
                if checkerOne == aRecord['e_name'] and checker[2] == aRecord['e_status'] and checker[3] == aRecord['e_time']:
                    print('An episode record has been existed:'+str(aRecord['s_id'])+':S'+str(aRecord['se_id'])+'E'+str(aRecord['e_num']))
                    dbc.close()
                    return "Repeat"
                else:
                    #self.log.takeLog('DEBUG','Before update a episode,record in db is :'+checker[1]+'|||'+checker[2]+'|||'+checker[3])
                    #self.log.takeLog('DEBUG','Before update a episode,record in py is :'+aRecord['e_name']+'|||'+aRecord['e_status']+'|||'+aRecord['e_time'])
                    sql = '''UPDATE `episode` SET `e_name` = \'%s\',`e_status` = \'%s\',`e_description` = \'%s\',`e_time` = \'%s\' WHERE `e_id` = \'%s\''''%(aRecord['e_name'],aRecord['e_status'],aRecord['e_description'],aRecord['e_time'],checker[0])
                    cursor.execute(sql)
                    dbc.commit()
                    print('An episode record has been updated:'+str(checker[0]))
                    #self.log.takeLog('DEBUG','An episode record has been updated:'+str(checker[0]))
                    dbc.close()
                    return "Update"
            else:
                sql = '''insert into episode(s_id,se_id,e_name,e_num,e_status,e_description,e_time) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'''%(aRecord['s_id'],aRecord['se_id'],aRecord['e_name'],aRecord['e_num'],aRecord['e_status'],aRecord['e_description'],aRecord['e_time'])
                cursor.execute(sql)
                dbc.commit()
                dbc.close()
                print('A record has been inserted:'+str(aRecord['s_id'])+':S'+str(aRecord['se_id'])+'E'+str(aRecord['e_num']))
                return "OK"
        except Exception, e:
            self.log.takeLog('ERROR','Table episode inserting error:'+ str(e)+' \nthe sql = '+sql+'\nthe e_name is %s'%(aRecord['e_name']))
            dbc.close()
            return "Error"
    def getOneLinkBySid(self,s_id):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlCheck = '''select link from shows where s_id = %s limit 1'''%(s_id)
            cursor.execute(sqlCheck)
            link = cursor.fetchone()
            dbc.close()
            if link == None:
                self.log.takeLog("WARNING","An empty select query has been requested. sql = "+ str(sqlCheck))
                return ""
            else:
                return link[0]
        except Exception, e:
            self.log.takeLog('ERROR','Table episode selecting error:'+ str(e)+' \nthe sql = '+sqlCheck)
            print(e)
            dbc.close()
            return "Error"
    def insertTag(self,showId,tagName):
        try:
            tagName = MySQLdb.escape_string(tagName)
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlCheck = '''select t_id from tag where t_name = \'%s\' limit 1'''%(tagName)
            sqlCheckStT = ''
            sqlInsToStT = ''
            sqlInsToTag = ''
            cursor.execute(sqlCheck)
            checker = cursor.fetchone()
            if checker:
                sqlCheckStT = '''select * from show_to_tag where s_id = %s and t_id = %s limit 1'''%(str(showId),str(checker[0]))
                cursor.execute(sqlCheckStT)
                checkerStT = cursor.fetchone()
                if checkerStT:
                    print('A tag relationship has been exist:tag_id-'+str(checker[0])+' to show_id-'+str(showId))
                    return "Repeat"
                else:
                    sqlInsToStT = '''insert into show_to_tag(s_id,t_id) values(%s,%s)'''%(showId,str(checker[0]))
                    cursor.execute(sqlInsToStT)
                    dbc.commit()
                    dbc.close()
                    print('A tag relationship has been set:tag_id-'+str(checker[0])+' to show_id-'+str(showId))
                    return "OK"
            else:
                sqlInsToTag = '''insert into tag(t_name) values(\'%s\')'''%(tagName)
                cursor.execute(sqlInsToTag)
                dbc.commit()
                self.insertTag(showId,tagName)
        except Exception, e:
            self.log.takeLog('ERROR','Table tag inserting error:'+ str(e))
            self.log.takeLog('DEBUG','the sqlCheck = '+sqlCheck)
            self.log.takeLog('DEBUG','the sqlCheckStT = '+sqlCheckStT)
            self.log.takeLog('DEBUG','the sqlInsToStT = '+sqlInsToStT)
            self.log.takeLog('DEBUG','the sqlInsToTag = '+sqlInsToTag)
            print(e)
            dbc.close()
            return "Error"
    def getAllTagWithoutCN(self):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sql = 'select t_id,t_name from tag where t_name_cn is null'
            cursor.execute(sql)
            rs = cursor.fetchall()
            dbc.close()
            return rs
        except Exception,e:
            print(e)
            self.log.takeLog('ERROR','Error in get tags from tag:'+ str(e)+'\n the sql='+sql)
            dbc.close()
            return
    def updateTagCN(self,t_id,t_name_cn):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlUpdate = '''UPDATE `tag` SET `t_name_cn` = \'%s\' WHERE `t_id` = %s'''%(t_name_cn,t_id)
            cursor.execute(sqlUpdate)
            dbc.commit()
            dbc.close()
            print('tag translated: '+ str(t_id) + t_name_cn)
            return "OK"
        except Exception,e:
            print(e)
            #print(sqlUpdate)
            self.log.takeLog('ERROR','Update table tag error:'+str(e)+'\n the sql='+sqlUpdate)
            dbc.close()
            return "Error"
    def getAllShowsWithoutCN(self):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sql = 'select s_id,s_name from shows where s_name_cn is null'
            cursor.execute(sql)
            rs = cursor.fetchall()
            dbc.close()
            return rs
        except Exception,e:
            print(e)
            self.log.takeLog('ERROR','Error in get tags from tag:'+ str(e)+'\n the sql='+sql)
            dbc.close()
            return
    def updateShowsCN(self,s_id,s_name_cn):
        try:
            dbc = self.connect()
            cursor = dbc.cursor()
            sqlUpdate = '''UPDATE `shows` SET `s_name_cn` = \'%s\' WHERE `s_id` = %s'''%(s_name_cn,s_id)
            cursor.execute(sqlUpdate)
            dbc.commit()
            dbc.close()
            print('show name translated: '+ str(s_id) + s_name_cn)
            return "OK"
        except Exception,e:
            print(e)
            #print(sqlUpdate)
            self.log.takeLog('ERROR','Update table shows.s_name_cn error:'+str(e)+'\n the sql='+sqlUpdate)
            dbc.close()
            return "Error"