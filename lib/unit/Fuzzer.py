from lib.core import fuzz
from lib.utils.Log import Log

class Fuzzer:
    def __init__(self,q):
        self.log = Log(__name__)
        self.q = q
        while True:
            if not self.q[0].empty():
                self.mission = self.q[0].get()
                break
    def run(self):
        while True:
            if not self.q[0].empty():
                data = self.q[0].get()
                tasks = fuzz(self.mission,data)
                self.q[1].put(tasks)
