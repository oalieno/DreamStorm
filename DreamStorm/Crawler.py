from lib.utils import connect

class Crawler:
    def __init__(self,q):
        self.q = q
    def run(self):
        while True:
            if not self.q[0].empty():
                package = self.q[0].get()
                result = connect(package["url"],package["headers"],package["postdata"])
                self.q[1].put(result)
