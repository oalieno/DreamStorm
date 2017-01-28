import Queue

class Internal(object):
    def __init__(self):
        self.qin = Queue.Queue()
        self.qout = Queue.Queue()
    def emptyin(self):
        return qin.empty()
    def emptyout(self):
        return qout.empty()
    def putin(self,data):
        self.qin.put(data)
    def putout(self,data):
        self.qout.put(data)
    def getin(self):
        try:
            return self.qin.get(timeout = 1)
        except Queue.Empty:
            return None
    def getout(self):
        try:
            return self.qout.get(timeout = 1)
        except Queue.Empty:
            return None
