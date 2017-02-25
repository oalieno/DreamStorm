import re

from bs4 import BeautifulSoup

from lib.utils.utils import appendQueries,iterate,connect

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
        task = {"type" : "page", "url" : url, "header" : header, "postdata" : postdata}
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
                task.append({"type" : "fuzz", "url" : appendQueries(url,queries), "header" : {}, "postdata" : {}})
            else:
                task.append({"type" : "fuzz", "url" : url, "header" : {}, "postdata" : queries})
        tasks += task
    return tasks

def analyze(mission,data):
    results = []
    soup = BeautifulSoup(data["response"],'lxml')

    # a fuzzing test has been responsed
    if data["type"] == "fuzz":
        results.append("the server response the fuzzing test")

    # iframes CSRF detection
    iframes = soup.find_all("iframe")
    for iframe in iframes:
        url = iframe.get("src")
        if "https://www.googletagmanager.com" not in url and iframe.get("width") == 0 and iframe.get("height") == 0:
            results.append(url + " -> an iframe contains this url and has width and height both 0 ( might be CSRF )")

    # images CSRF detection
    images = soup.find_all("img")
    for image in images:
        url = image.get("src")
        if url:
            page,info = connect(url)
        if info.get("Content-Type") and "image" not in info["Content-Type"]:
            results.append(url + " -> this image didn't response with image, it response with type " + info["Content-Type"] + " ( might be CSRF )")

    return [{"type" : "vulnerability", "url" : data["url"], "header" : data["header"], "postdata" : data["postdata"], "data" : results}]

def collect(mission,data):
    soup = BeautifulSoup(data["response"],'lxml')
    items = soup.select(mission["css-selector"])
    return [{"type" : "collection", "url" : data["url"], "header" : data["header"], "postdata" : data["postdata"], "data" : [item.string for item in items if item.string]}]

def version(mission,data):
    results = []
    if data["response-header"].get("server"):
        results = [{"type" : "vulnerability", "url" : data["url"], "header" : data["header"], "postdata" : data["postdata"], "data" : "The server type and version is : " + data["response-header"]["server"]}]
    return results
