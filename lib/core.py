import re
import json
import subprocess

from bs4 import BeautifulSoup

from lib.utils.utils import appendQueries,iterate,connect,package

def absolute(myrange,domain,url,append):
    if not append:
        return None
    if re.search("^//",append) != None:
        return None

    # If don't have http or https prefix
    if re.search("^https?://",append) == None:
        # absolute url
        if append[0] == '/':
            append = domain + '/' + append.strip('/')
        # relative url
        else:
            append = url + '/' + append.strip('/')
    append = append.partition('#')[0].strip('/')

    if myrange == "domain" and domain not in append:
        append = None
    if myrange == "subdomain" and url not in append:
        append = None
    if myrange == "page":
        append = None
    return append

def page(mission,data,urllist):
    soup = BeautifulSoup(data['response'],'lxml')
    urls = soup.find_all('a')
    tasks = []
    for url in urls:
        url = absolute(mission["range"],mission["domain"],mission["url"],url.get('href'))
        if url and url not in urllist:
            urllist.append(url)
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

def fuzz(mission,data,urllist):
    tasks = []
    soup = BeautifulSoup(data["response"],'lxml')
    forms = soup.find_all("form")
    for form in forms:
        url = absolute(mission["range"],mission["domain"],mission["url"],form.get("action"))
        if not url:
            continue
        method = form.get("method").lower()
        keys = [i["name"] for i in form.find_all("input") + form.find_all("select") if i.get("name")]
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

    # iframes CSRF detection
    iframes = soup.find_all("iframe")
    for iframe in iframes:
        url = iframe.get("src")
        if url and "https://www.googletagmanager.com" not in url and iframe.get("width") == 0 and iframe.get("height") == 0:
            results.append(url + " -> an iframe contains this url and has width and height both 0 ( might be CSRF )")

    # images CSRF detection
    images = soup.find_all("img")
    for image in images:
        url = image.get("src")
        if url:
            page,info = connect(url)
        if info.get("Content-Type") and "image" not in info["Content-Type"]:
            results.append(url + " -> this image didn't response with image, it response with type " + info["Content-Type"] + " ( might be CSRF )")

    return [package("vulnerability",data,results)]

def collect(mission,data):
    results = []
    if mission.get("css-selector"):
        soup = BeautifulSoup(data["response"],'lxml')
        items = soup.select(mission["css-selector"])
        results = [package("collection",data,[item.string for item in items if item.string])]
    return results

def version(mission,data,versionlist):
    results = []
    if data["response-header"].get("server"):
        servers = []
        for server in data["response-header"]["server"].split():
            server = server.strip()
            if not ( server[0] == '(' and server[-1] == ')' ):
                servers.append(server)
        for server in servers:
            if server in versionlist:
                continue
            versionlist.append(server)

            _ = server.partition('/')
            framework = _[0]
            version = _[1]

            cve = subprocess.check_output(["searchsploit",framework + ' ' + version,"-wj"])
            cve = cve[cve.find('[')+1:cve.find(']')].split('\n')
            cve = [ (_.split('|')[0].strip(),_.split('|')[1].strip()) for _ in cve if _.find('|') != -1 ]
            if cve:
                message = "The server type and version : " + server + " which has " + str(len(cve)) + " cve exploits found!"
                for i in xrange(min(len(cve),3)):
                    message += "\n" + " "*18 + cve[i][0] + " -> " + cve[i][1]
                results.append(package("vulnerability",data,message))
    return results
