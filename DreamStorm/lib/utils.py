# -*- coding: utf-8 -*-

import socks
import socket
import urllib
import urllib2
import threading


def daemonThread(target, args=()):
    t = threading.Thread(target=target, args=args)
    t.daemon = True
    t.start()


def tor_init():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket


def connect(package):
    url = package["url"]
    headers = package["headers"]
    postdata = urllib.urlencode(package["postdata"])
    try:
        if postdata:
            request = urllib2.Request(url, headers=headers, data=postdata)
        else:
            request = urllib2.Request(url, headers=headers)
        opener = urllib2.build_opener()
        response = opener.open(request)
    except:
        return package, "", {}
    page = response.read()
    info = dict(response.info())
    return package, page, info
