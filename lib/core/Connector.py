import socks
import urllib2

class Connector:
    def __init__(self,config):
        self.config = config
    def run(self,tunnel):
        if self.config.get('tor'):
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
            socket.socket = socks.socksocket
        while True:
            if not tunnel.emptyin():
                task = tunnel.getin()
                try:
                    if task.get("postdata"):
                        request = urllib2.Request(task.get("url"),headers = task.get("header"),data = task.get("postdata"))
                    else:
                        request = urllib2.Request(task.get("url"),headers = task.get("header"))
                    opener = urllib2.build_opener()
                    response = opener.open(request)
                except:
                    tunnel.putout(dict(task.items() + {"response" : ""}.items()))
                    continue
                page = response.read()
                tunnel.putout(dict(task.items() + {"response" : page}.items()))
