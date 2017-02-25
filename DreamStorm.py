#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from lib.unit.Manager import Manager
from lib.utils.Config import check
from lib.utils.Log import Log

log = Log(__name__)

# Load config and missions
with open('config.json','r') as data:
    try:
        config = json.load(data)
    except ValueError as error:
        log.error("In config.json : " + str(error))

with open("missions.json",'r') as data:
    try:
        missions = json.load(data)
    except ValueError as error:
        log.error("In missions.json : " + str(error))

check(config,missions)

m = Manager(config,missions)
m.run()
