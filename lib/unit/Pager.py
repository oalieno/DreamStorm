from lib.core import page
from lib.utils.Log import Log

class Pager:
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
                tasks = page(self.mission,data,wholelist)
                self.q[1].put(tasks)
