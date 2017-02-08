import socks

from lib.core import connect 

class Connector:
    def __init__(self,q):
        self.q = q
        while True:
            if not self.q[0].empty():
                self.config = self.q[0].get()
                break
    def run(self):
        if self.config.get('tor'):
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
            socket.socket = socks.socksocket
        while True:
            if not self.q[0].empty():
                task = self.q[0].get()
                page = connect(task["url"],task["header"],task["postdata"])
                self.q[1].put(dict(task.items() + {"response" : page}.items()))
