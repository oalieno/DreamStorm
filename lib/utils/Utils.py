import re
import json
import threading

with open("source/common-name-list.txt","r") as data:
    names = data.read().strip().split('\n')

def iterate(initial,distance):
    if type(initial) is int:
        return initial + distance
    elif type(initial) is str:
        if initial:
            return initial if distance == 0 else names[distance-1]
        else:
            return names[distance]

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
