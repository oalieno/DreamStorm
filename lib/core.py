import re
import urllib
import urllib2

from bs4 import BeautifulSoup

from lib.utils.Utils import appendQueries,iterate

def absolute(myrange,domain,url,append):
    if append == None:
        return None
    if re.search("^//",append) != None:
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

def mutate(mutations,initials,mode):
    results = []
    statusTotal = mutations ** len(initials)
    for status in xrange(statusTotal):
        now = []
        for initial in initials:
            now.append(iterate(initial,status % mutations,mode))
            status /= mutations
        results.append(now)
    return results

def generate(mission,url):
    tasks = []
    initials = []
    url = appendQueries(url,mission.get('stable-query'))
    header = mission.get('stable-header')
    postdata = mission.get('stable-postdata')
    for key,value in mission["mutable-query"].iteritems():
        initials.append(value)
    for key,value in mission['mutable-header'].iteritems():
        initials.append(value)
    for key,value in mission['mutable-postdata'].iteritems():
        initials.append(value)
    results = mutate(mission["mutations"],initials,"default")
    for result in results:
        now = 0
        task = {"url" : url, "header" : header, "postdata" : postdata}
        for key,value in mission["mutable-query"].iteritems():
            task["url"] = appendQueries(task["url"],result[now])
            now += 1
        for key,value in mission['mutable-header'].iteritems():
            task["header"][key] = result[now]
            now += 1
        for key,value in mission['mutable-postdata'].iteritems():
            task["postdata"][key] = result[now]
            now += 1
        tasks.append(task)
    return tasks

def fuzz(mission,data):
    tasks = []
    soup = BeautifulSoup(data["response"],'lxml')
    forms = soup.find_all("form")
    for form in forms:
        url = absolute(mission["range"],mission["domain"],mission["url"],form.get("action"))
        method = form.get("method").lower()
        keys = [i.get("name") for i in form.find_all("input") + form.find_all("select")]
        results = mutate(5,[""] * len(keys),"sqli")
        task = []
        for result in results:
            queries = {}
            for i,key in enumerate(keys):
                queries[key] = result[i]
            if method == "get":
                task.append({"url" : appendQueries(url,queries), "header" : {}, "postdata" : {}})
            else:
                task.append({"url" : url, "header" : {}, "postdata" : queries})
        tasks += task
    return tasks

def connect(url,header,postdata):
    postdata = urllib.urlencode(postdata)
    try:
        if postdata:
            request = urllib2.Request(url,headers = header,data = postdata)
        else:
            request = urllib2.Request(url,headers = header)
        opener = urllib2.build_opener()
        response = opener.open(request)
    except:
        return ""
    page = response.read().decode("utf-8","ignore")
    return page
