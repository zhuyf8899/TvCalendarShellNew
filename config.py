#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
class Config(object):
	"""settings like url and so on."""
	def __init__(self):
		pass
	#the url we will reach
	url = 'http://www.pogdesign.co.uk'
	urlAllShows = 'http://www.pogdesign.co.uk/cat/all-shows/'

	#the database host we looking for
	dataBaseHost = "localhost"

	#the database username
	dataBaseUser = "username"

	#the password of the username metioned above
	dataBasePwd = "password"

	#default table
	dataBasedb = "TvCalandar"
	
#author: zhuyifan
		