#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#config.py:配置文件
class Config(object):
	"""settings like url and so on."""
	def __init__(self):
		pass
	#the url we will reach
	url = 'http://www.pogdesign.co.uk'
	transURL = 'http://fanyi.youdao.com/openapi.do?keyfrom=TVCalendarCN&key=<akeyfromyoudao>type=data&doctype=json&version=1.1&q='
	urlAllShows = 'http://www.pogdesign.co.uk/cat/all-shows/'

	#the database host we looking for
	dataBaseHost = "localhost"

	#the database username
	dataBaseUser = "username"

	#the password of the username metioned above
	dataBasePwd = "password"

	#default table
	dataBasedb = "TvCalandar"

	#the host of resource database
	dataBaseHostRes = 'localhost'

	#the resource database username 
	dataBaseUserRes = 'username'

	#the password
	dataBasePwdRes = 'password'

	#the database
	dataBasedbRes = 'resource'
	
#author: zhuyifan
		