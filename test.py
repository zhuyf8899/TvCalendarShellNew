#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#test.py:用于调试的测试程序
#note:有一个bug，出现在源中存在12：30pm，此时不能正确处理时间，复现步骤：slect * from episode where s_id = 7
from config import Config
from readHtml import Reader
from log import Log
from tools import Tools

config = Config()
reader = Reader(config)
#tools = Tools(config)
#tools.workWithOneShowsEp(1)
#reader.allShowsWork()
reader.finishAllShows(True)
#reader.testerInEpisode()

print("Done.")
