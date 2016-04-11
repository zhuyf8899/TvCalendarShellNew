#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#test.py:用于调试的测试程序
#发现一个新的bug，见日志：out of index
from config import Config
from readHtml import Reader
from log import Log
from tools import Tools

config = Config()
reader = Reader(config)
#tools = Tools(config)
#tools.flush_one_page('0')
#tools.workWithOneShowsEp(1026)
#tools.workWithOneShowsEp(1023)
#tools.workWithOneShowsEp(1402)
#tools.workWithOneShowsEp(1403)

reader.allShowsWork()
reader.finishAllShows(False)
#reader.testerInEpisode()

print("Done.")
