#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb


#conn = MySQLdb.connect(host="localhost",user="root",passwd="123123",db="qiwsirtest",port=3306,charset="utf8")
class Database(object):
	def __init__(h,u,p,d,fileHandler):
		self.host = h
		self.user = u
		self.passwd = p
		self.db = d
		self.fileHandler = fileHandler
	def __init__(self,fileHandler,config):
		self.host = config.dataBaseHost
		self.user = config.dataBaseUser
		self.passwd = config.dataBasePwd
		self.db = config.dataBasedb
		self.fileHandler = fileHandler
	def __init__(self,config):
		self.host = config.dataBaseHost
		self.user = config.dataBaseUser
		self.passwd = config.dataBasePwd
		self.db = config.dataBasedb
		#self.fileHandler = fileHandler
	def connect(self):
		try:
			conn = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,charset='utf8')
		except Exception, e:
			print(e)
			#self.fileHandler.write(str(e))
			return "connectError"
		return conn
	def insertShowFirstTime(self,obj):#obj中必须有s_name,link,status和s_sibox_image
		try:
			dbc = self.connect()
			cursor = dbc.cursor()
			sqlCheck = '''select s_id,s_name,status,s_sibox_image,link from shows where s_name = \"%s\"'''%(obj['s_name'])
			cursor.execute(sqlCheck)
			checker = cursor.fetchone()
			#print(checker)
			if checker:
				if checker[2] == obj['status'] and checker[3] == obj['s_sibox_image'] and checker[4] == obj['link']:
					dbc.close()
					print("repeat\n")
					return "Repeat"
				else:
					sqlUpdate = '''UPDATE `shows` SET  `status` =  \'%s\',`s_sibox_image` =  \'%s\',`link` =  \'%s\' WHERE  `shows`.`s_id` = %s;'''%(obj['status'],obj['s_sibox_image'],obj['link'],checker[0])
					cursor.execute(sqlUpdate)
					dbc.commit()
					dbc.close()
					print('update\n')
					return "Update"
			else:
				sqlInsert = '''insert into shows(s_name,status,s_sibox_image,link) values(\"%s\",\"%s\",\"%s\",\"%s\")'''%(obj['s_name'],obj['status'],obj['s_sibox_image'],obj['link'])
				cursor.execute(sqlInsert)
				dbc.commit()
				dbc.close()
				print('insert')
				return "OK"
		except Exception,e:
			print(e)
			dbc.close()
			return "Error"

	def updateShowDetail(self,obj):#obj中必须有s_id,s_description,update_time,area,channel和length
		try:
			dbc = self.connect()
			cursor = dbc.cursor()
			sqlUpdate = '''UPDATE `shows` SET `s_description` = \'%s\',`update_time` = \'%s\',`area` = \'%s\',`length` = \'%s\',`channel` = \'%s\' WHERE `s_id` = \'%s\''''%(obj['s_description'],obj['update_time'],obj['area'],obj['length'],obj['channel'],obj['s_id'])
			cursor.execute(sqlUpdate)
			dbc.commit()
			dbc.close()
			print('update')
			return "Finished"
		except Exception,e:
			print(e)
			print(sqlUpdate)
			dbc.close()
			exit()
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
			dbc.close()
			return "Error"
	# def getAllNames(self):
	# 	try:
	# 		dbc = self.connect()
	# 		cursor = dbc.cursor()
	# 		sql = "select * from name"
	# 		cursor.execute(sql)
	# 		datas = cursor.fetchall()	
	# 	except Exception, e:
	# 		print(e)
	# 		self.fileHandler.write(str(e))
	# 		dbc.close()
	# 		return "SelectError"
	# 	#for data in datas:
	# 	#	print(data)
	# 	dbc.close()
	# 	return datas
	# def insertName(self,name,photoLink):
	# 	db = self.connect()
	# 	cursor = db.cursor()
	# 	try:
	# 		sql = '''insert into name(n_name,n_photoLink) values(\"%s\",\"%s\")'''%(name,photoLink)
	# 		cursor.execute(sql)
	# 		db.commit()
	# 		self.fileHandler.write('''NOTICE: Insert a name:%s'''%(name))
	# 		sql = '''select n_id from name where n_name = \"%s\"'''%(name)
	# 		cursor.execute(sql)
	# 		data = cursor.fetchone()
	# 		db.close()
	# 		return data
	# 	except Exception, e:
	# 		if e[0] == 1062: #means Duplicate entry
	# 			sql = '''select n_id from name where n_name = \"%s\"'''%(name)
	# 			cursor.execute(sql)
	# 			data = cursor.fetchone()
	# 			db.close()
	# 			return data
	# 		else:
	# 			print(e)
	# 			self.fileHandler.write(str(e))
 #    			db.rollback()
 #    			db.close()
 #    			return "InsertError"
    	
	# def insertEpisode(self,n_id,e_season,e_espisode,e_name,e_onAir,e_descirption):
	# 	db = self.connect()
	# 	cursor = db.cursor()
	# 	sql = '''insert into episode(n_id,e_season,e_episode,e_name,e_onAir,e_description) values(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")'''%(n_id,e_season,e_espisode,e_name,e_onAir,e_descirption)
	# 	try:
	# 		cursor.execute(sql)
	# 		db.commit()
	# 	except Exception, e:
	# 		if e[0] == 45001: #means tri_protect
	# 			db.close()
	# 			return "RecordProtect"
	# 		else:
	# 			print(e)
	# 			self.fileHandler.write(str(e))
	# 			db.rollback()
	# 			db.close()
	# 			return "InsertError"
	# 	db.close()
	# 	return "ok"
	# def getLastDay(self):
	# 	db = self.connect()
	# 	cursor = db.cursor()
	# 	sql = "select c_value from config where c_name = \"lastDay\" limit 1"
	# 	try:
	# 		cursor.execute(sql)
	# 		data = cursor.fetchone()
	# 	except Exception, e:
	# 		print(e)
	# 		self.fileHandler.write(str(e))
	# 		db.close()
	# 		return "SelectError"
	# 	db.close()
	# 	return data
	# def updateLastDay(self,ld):
	# 	db = self.connect()
	# 	cursor = db.cursor()
	# 	sql = "update config set c_value = \"%s\" where c_name = \"lastDay\""%(ld)
	# 	try:
	# 		cursor.execute(sql)
	# 		db.commit()
	# 	except Exception, e:
	# 		print(e)
	# 		self.fileHandler.write(str(e))
	# 		db.rollback()
	# 		db.close()
	# 		return "UpdateError"
	# 	db.close()
	# 	return True
#Author:zhuyifan on 11-5-2015 in Beijing
		
