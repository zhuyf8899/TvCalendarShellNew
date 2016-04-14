#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#test.py:用于调试的测试程序

from config import Config
from readHtml import Reader
from log import Log
from tools import Tools
from translator import Translator

config = Config()
reader = Reader(config)
translator = Translator(config)
tools = Tools(config)

#更新某一字母开头的页面全部剧简略信息的方法，对应于reader.allShowsWork()的单步
#tools.flush_one_page('T')

#更新某部剧，其中参数为剧在数据库中的s_id,对应于#reader.finishAllShows(True)的单步
#tools.workWithOneShowsEp(1026)

#reader.allShowsWork()
#reader.finishAllShows(False)

#translator.transTag()
#translator.transShow()

print("Test Done.")
