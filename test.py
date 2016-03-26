#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#test.py:用于调试的测试程序
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
