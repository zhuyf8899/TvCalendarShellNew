#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#start.py:程序入口

from config import Config
from readHtml import Reader
from log import Log
from translator import Translator
import sys
#引入模块:config - 配置文件
#		 readHtml - TVCalendar页面解析器
#		 log - 日志组件
#		 translator - 翻译组件
#		 sys - 官方的sys模块

#另:用户可在test.py文件中使用Tools类进行调试，具体请参考test.py

#用法：python start.py <Ture|False>
#第一次执行脚本时请使用True参数，之后使用False.
#True时脚本将更新整个数据库而False则是仅更新新剧集
flag = False
if sys.argv[1] == 'True':
	flag = True

config = Config()
reader = Reader(config)
translator = Translator(config)

#更新全部的剧的简略信息
reader.allShowsWork()
#更新全部剧的详细信息和其附属的全部集，前置条件为allShowWork()已被调用
reader.finishAllShows(flag)

#翻译器翻译全部没有中文译名的标签
translator.transTag()
#翻译器翻译全部没有中文译名的剧名
#注:目前使用的有道翻译API是存在过热的情况（每小时调用不超过1000次），因此这里存在阈值950，如果需要调整则使用以下形式的调用
#translator.transShow(counter)#counter为调用翻译API的次数
translator.transShow()


print('done.')