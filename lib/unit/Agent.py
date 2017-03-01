import hashlib

from lib.core import page,fuzz,analyze,collect,version
from lib.utils.Log import Log

class Agent:
    def __init__(self,q):
        self.q = q
        while True:
            if not self.q[0].empty():
                self.mission = self.q[0].get()
                break
    def run(self):
        urllist = [self.mission['url']]
        pagelist = {}
        while True:
            if not self.q[0].empty():
                data = self.q[0].get()
                abstract = hashlib.sha256(data["response"].encode('utf-8','ignore')).hexdigest()
                results = []
                # We haven't seen this page yet
                if not pagelist:
                    results += version(self.mission,data)
                if data["type"] != "fuzz":
                    if pagelist.get(abstract) == None:
                        results += page(self.mission,data,urllist)
                        results += analyze(self.mission,data)
                        results += collect(self.mission,data)
                        pagelist[abstract] = [1,data]
                    else:
                        pagelist[abstract][0] += 1
                    if self.mission["fuzzing"]:
                        results += fuzz(self.mission,data,urllist)
                self.q[1].put(results)
                #print [pagelist[key][1]["url"] for key in pagelist if pagelist[key][0] == 1]
