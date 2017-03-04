import socks
import socket

from lib.utils.utils import connect,tor

class Connector:
    def __init__(self,q):
        self.q = q
        while True:
            if not self.q[0].empty():
                self.config = self.q[0].get()
                break
    def run(self):
        if self.config['Connector-tor']:
            tor()
        while True:
            if not self.q[0].empty():
                task = self.q[0].get()
                page,info = connect(task["url"],task["header"],task["postdata"])
                self.q[1].put(dict(task.items() + {"response" : page, "response-header" : info}.items()))
