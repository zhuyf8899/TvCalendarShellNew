#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from config import Config
from readHtml import Reader
from log import Log

config = Config()
reader = Reader(config)
log = Log()
log.takeLog('ERROR',"We have a test here.")
log.takeLog('WARNING',"it is a warning.")
log.takeLog('INFO',"it is an info.")

#reader.testerInEpisode()

print("FUCK")
