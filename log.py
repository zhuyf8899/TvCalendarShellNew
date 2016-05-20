#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#log.py:日志模块
import time
import os

class Log(object):
	def __init__(self):
		super(Log, self).__init__()
		self.path = "./logs"
		if os.path.exists(self.path):
			pass
		else:
			os.makedirs(self.path)
	def takeLog(self,level,report):
	 	fileName = time.strftime("%Y-%m-%d", time.localtime())
	 	fileName += '.log'
	 	fileWholePath = self.path + '/' + fileName
	 	try:
		 	if not os.path.exists(fileWholePath):
		 		fileHandler = open(fileWholePath,'w')
		 	else:
		 		fileHandler = open(fileWholePath,'a')
		except Exception, e:
			print('FATAL ERROR: Opening log file error - ' + str(e))
			if fileHandler != None:
				fileHandler.close()
			exit(-1)
		try:
			logReport = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '[' + str(level) + ']:' + str(report)
	 		fileHandler.write(logReport+'\n')
	 		fileHandler.close()
		except Exception, e:
			print('FATAL ERROR: Writing log file error - ' + str(e))
			fileHandler.close()
			exit(-2)
	 	return