import sys
import Queue

from lib.remote.Client import Client
from lib.unit.Connector import Connector

q = (Queue.Queue(),Queue.Queue())
client = Client(q,sys.argv[1],int(sys.argv[2]))
c = Connector(q)
c.run()
