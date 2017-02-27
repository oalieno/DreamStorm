#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Queue

from lib.remote.Client import Client
from lib.unit.Connector import Connector
from lib.utils.Utils import daemonThread

q = (Queue.Queue(),Queue.Queue())
client = Client(q)
daemonThread(client.listen,(sys.argv[1],int(sys.argv[2])))
c = Connector(q)
c.run()
