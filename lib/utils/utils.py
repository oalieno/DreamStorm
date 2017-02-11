import re
import json
import socks
import socket
import urllib
import urllib2
import threading

with open("source/common-name-list.txt","r") as data:
    names = data.read().strip().split('\n')
with open("source/generic-sqli.txt","r") as data:
    sqlis = data.read().strip().split('\n')

def iterate(initial,distance,mode):
    if type(initial) is int:
        return initial + distance
    elif type(initial) is str:
        if mode == "default":
            if initial:
                return initial if distance == 0 else names[distance-1]
            else:
                return names[distance]
        elif mode == "sqli":
            return sqlis[distance]

nonspace = re.compile(r'\S')

def iterParse(j):
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded

def daemonThread(target,args = ()):
    t = threading.Thread(target = target,args = args)
    t.daemon = True
    t.start()

def appendQueries(url,queries):
    if queries:
        if '?' not in url:
            url += '?'
        for key,value in queries.iteritems():
            if url[-1] != '?':
                url += '&'
            url += key + '=' + str(value)
    return url

def tor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
    socket.socket = socks.socksocket

def connect(url,header = {},postdata = {}):
    postdata = urllib.urlencode(postdata)
    try:
        if postdata:
            request = urllib2.Request(url,headers = header,data = postdata)
        else:
            request = urllib2.Request(url,headers = header)
        opener = urllib2.build_opener()
        response = opener.open(request)
    except:
        return "",{}
    page = response.read().decode("utf-8","ignore")
    info = response.info()
    return page,info
