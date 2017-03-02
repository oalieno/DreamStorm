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
        versionlist = []
        while True:
            if not self.q[0].empty():
                data = self.q[0].get()
                results = []
                results += version(self.mission,data,versionlist)
                results += page(self.mission,data,urllist)
                results += analyze(self.mission,data)
                results += collect(self.mission,data)
                #if self.mission["fuzzing"]:
                #    results += fuzz(self.mission,data,urllist)
                self.q[1].put(results)
