import socket
import redis

class DB:
    def __init__(self):
        self.r = redis.Redis(host = "localhost", port = 6379, db = 0)
    def store(self,data):
        self.r.hset(data["type"],data["url"] + str(data["header"]) + str(data["postdata"]), str(data["data"]))
    def storeall(self,data):
        for d in data:
            self.store(d)
