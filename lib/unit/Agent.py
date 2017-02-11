from lib.core import page,fuzz,analyze,collect
from lib.utils.Log import Log

class Agent:
    def __init__(self,q):
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
                results = page(self.mission,data,wholelist)
                if self.mission["fuzzing"]:
                    results += fuzz(self.mission,data)
                results += analyze(self.mission,data)
                results += collect(self.mission,data)
                self.q[1].put(results)
