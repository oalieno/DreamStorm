#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Queue

from lib.remote.Client import Client
from lib.unit.Connector import Connector
from lib.utils.Utils import daemonThread
from lib.utils.Log import Log

log = Log(__name__)

if len(sys.argv) != 3:
    log.info("usage : ./Connector-Client.py (ip) (port)")
    sys.exit(0)

q = (Queue.Queue(),Queue.Queue())
client = Client(q)
daemonThread(client.listen,(sys.argv[1],int(sys.argv[2])))
c = Connector(q)
c.run()
