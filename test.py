#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#test.py:用于调试的测试程序
from config import Config
from readHtml import Reader
from log import Log

config = Config()
reader = Reader(config)
reader.allShowsWork()
reader.finishAllShows()
#reader.testerInEpisode()

print("FUCK")
