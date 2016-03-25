#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
from config import Config
from readHtml import Reader

config = Config()
reader = Reader(config)

reader.testerInEpisode()
print("FUCK")
