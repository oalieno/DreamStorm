import socks
import socket
import urllib
import urllib2
import threading

def daemonThread(target,args = ()):
    t = threading.Thread(target = target,args = args)
    t.daemon = True
    t.start()

def tor_init():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
    socket.socket = socks.socksocket

def connect(url,headers,postdata):
    postdata = urllib.urlencode(postdata)
    try:
        if postdata:
            request = urllib2.Request(url,headers = headers,data = postdata)
        else:
            request = urllib2.Request(url,headers = headers)
        opener = urllib2.build_opener()
        response = opener.open(request)
    except:
        return "",{}
    page = response.read().decode("utf-8","ignore")
    info = dict(response.info())
    return page,info
