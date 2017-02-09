from lib.core import page,fuzz,analyze
from lib.utils.Log import Log

class Agent:
    def __init__(self,q):
        self.log = Log(__name__)
        self.q = q
        while True:
            if not self.q[0].empty():
                self.mission = self.q[0].get()
                break
    def run(self):
        wholelist = [self.mission['url']]
        while True:
            if not self.q[0].empty():
                data = self.q[0].get()
                self.log.info(data["url"])
                results = page(self.mission,data,wholelist)
                results += fuzz(self.mission,data)
                results += analyze(self.mission,data)
                self.q[1].put(results)
