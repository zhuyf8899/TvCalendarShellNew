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
#tools = Tools(config)

#tools.flush_one_page('T')
#tools.workWithOneShowsEp(1026)
#tools.workWithOneShowsEp(1023)
#tools.workWithOneShowsEp(1402)
#tools.workWithOneShowsEp(1403)


#reader.allShowsWork()
#reader.finishAllShows(False)
#reader.testerInEpisode()

translator.transTag()
translator.transShow()

print("Done.")
