import os
import re

from bs4 import BeautifulSoup

from lib.utils.Log import Log

class Agent:
    def __init__(self,mission):
        self.log = Log(__name__)
        self.mission = mission
    def absolute(self,url):
        if url == None:
            return None
        if re.search("^https?://",url) == None:
            url = self.mission['domain'] + '/' + url.strip('/')
        url = url.partition('#')[0]
        if self.mission['range'] == "domain" and self.mission['domain'] not in url:
            url = None
        if self.mission['range'] == "subdomain" and self.mission['url'] not in url:
            url = None
        if self.mission['range'] == "page":
            url = None
        return url
    def append_queries(self,url,queries):
        if queries:
            if '?' not in url:
                url += '?'
            for key,value in queries.iteritems():
                if url[-1] != '?':
                    url += '&'
                url += key + '=' + str(value)
        return url
    def generate(self,url):
        tasks = []
        url = self.append_queries(url,self.mission.get('stable-query'))
        header = self.mission.get('stable-header')
        postdata = self.mission.get('stable-postdata')
        with open("source/common-name-list.txt","r") as data:
            names = data.read().strip().split('\n')
        table = []
        for key,value in self.mission['mutable-query'].iteritems():
            table.append({"type" : "query", "key" : key, "value" : value})
        for key,value in self.mission['mutable-header'].iteritems():
            table.append({"type" : "header", "key" : key, "value" : value})
        for key,value in self.mission['mutable-postdata'].iteritems():
            table.append({"type" : "postdata", "key" : key, "value" : value})
        mutations = self.mission['mutations']
        status_total = mutations**len(table)
        for status in xrange(status_total):
            task = {"url" : url, "header" : header, "postdata" : postdata}
            for mutation in table:
                if type(mutation["value"]) == int:
                    value = mutation["value"] + status % mutations
                else:
                    # Make the user input be one of the values
                    if status % mutations == 0 and mutation['value']:
                        value = mutation['value']
                    else:
                        value = names[status % mutations - 1] if mutation["value"] else names[status % mutataions]
                if mutation["type"] == "query":
                    task["url"] = self.append_queries(task["url"],{mutation["key"] : value})
                else:
                    task[mutation["type"]] = dict(task[mutation["type"]].items() + {mutation["key"] : value}.items())
                status /= mutations
            tasks.append(task)
        return tasks
    def analyze(self,response):
        self.log.info(response['url'])
    def run(self,tunnel):
        wholelist = []
        while True:
            if not tunnel.emptyin():
                data = tunnel.getin()
                self.analyze(data)
                soup = BeautifulSoup(data['response'].decode('utf-8', 'ignore'),'lxml')
                urls = soup.find_all('a')
                tasks = []
                for url in urls:
                    url = self.absolute(url.get('href'))
                    if url and url not in wholelist:
                        wholelist.append(url)
                        tasks += self.generate(url)
                tunnel.putout(tasks)
    def report(self):
        pass 
