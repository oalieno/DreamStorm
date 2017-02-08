import re
import urllib2

from bs4 import BeautifulSoup

from lib.utils.Utils import appendQueries

def absolute(myrange,domain,url,append):
    if append == None:
        return None
    if re.search("^https?://",append) == None:
        append = domain + '/' + append.strip('/')
    append = append.partition('#')[0].strip('/')
    if myrange == "domain" and domain not in append:
        append = None
    if myrange == "subdomain" and url not in append:
        append = None
    if myrange == "page":
        append = None
    return append

def page(mission,data,wholelist):
    soup = BeautifulSoup(data['response'],'lxml')
    urls = soup.find_all('a')
    tasks = []
    for url in urls:
        url = absolute(mission["range"],mission["domain"],mission["url"],url.get('href'))
        if url and url not in wholelist:
            wholelist.append(url)
            tasks += generate(mission,url)
    return tasks

def generate(mission,url):
    tasks = []
    url = appendQueries(url,mission.get('stable-query'))
    header = mission.get('stable-header')
    postdata = mission.get('stable-postdata')
    table = []
    for key,value in mission['mutable-query'].iteritems():
        table.append({"type" : "query", "key" : key, "value" : value})
    for key,value in mission['mutable-header'].iteritems():
        table.append({"type" : "header", "key" : key, "value" : value})
    for key,value in mission['mutable-postdata'].iteritems():
        table.append({"type" : "postdata", "key" : key, "value" : value})
    mutations = mission['mutations']
    statusTotal = mutations**len(table)
    for status in xrange(statusTotal):
        task = {"url" : url, "header" : header, "postdata" : postdata}
        for mutation in table:
            value = iterate(mutation["value"],status % mutations)
            if mutation["type"] == "query":
                task["url"] = appendQueries(task["url"],{mutation["key"] : value})
            else:
                task[mutation["type"]] = dict(task[mutation["type"]].items() + {mutation["key"] : value}.items())
            status /= mutations
        tasks.append(task)
    return tasks

def fuzz(mission,data):
    tasks = []
    return tasks

def connect(url,header,postdata):
    try:
        if postdata:
            request = urllib2.Request(url,headers = header,data = postdata)
        else:
            request = urllib2.Request(url,headers = header)
        opener = urllib2.build_opener()
        response = opener.open(request)
    except:
        return ""
    page = response.read().decode("utf-8", "ignore")
    return page
