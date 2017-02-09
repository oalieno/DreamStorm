import Queue

from lib.remote.Server import Server
from lib.unit.Agent import Agent
from lib.unit.Connector import Connector
from lib.utils.Utils import daemonThread

class Manager:
    def __init__(self,config,missions):
        self.config = config
        self.missions = missions
    def run(self):
        '''
        Connector tunnel in : {"index" : integer, "type" : string, "url" : string, "header" : dictionary, "postdata" : dictionary}
        Connector tunnel out : {"index" : integet, "type" : string, "url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
        '''

        '''
        Agent tunnel in : {"type" : string, "url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
        Agent tunnel out : [{"type" : string, "url" : string, "header" : dictionary, "postdata" : dictionary},...]
        '''

        # queue-in and queue-out
        aQueue = [(Queue.Queue(),Queue.Queue()) for i in xrange(len(self.missions))]
        cQueue = [(Queue.Queue(),Queue.Queue()) for i in xrange(self.config["Connector-threads"])]

        # send config and missions
        for i,mission in enumerate(self.missions):
            aQueue[i][0].put(mission)
        for i in xrange(self.config["Connector-threads"]):
            cQueue[i][0].put(self.config)

        # start pager locally
        for i,mission in enumerate(self.missions):
            a = Agent(aQueue[i])
            daemonThread(a.run)

        if self.config["mode"] == "local":
            # start connectors locally
            for i in xrange(self.config["Connector-threads"]):
                c = Connector(cQueue[i])
                daemonThread(c.run)
        else:
            # start connectors remotely
            cServer = Server()
            for i in xrange(self.config["Connector-threads"]):
                cServer.addTunnel(cQueue[i])
            daemonThread(cServer.listen,(self.config["ip"],self.config["port"]))

        aCounter = 0
        cCounter = 0

        connectorNext = 0
        connectorTotal = self.config["Connector-threads"]

        # put initial tasks
        for i,mission in enumerate(self.missions):
            if self.config["mode"] == "remote":
                while not cServer.alives[connectorNext]:
                    connectorNext = (connectorNext + 1) % connectorTotal
            cQueue[connectorNext][0].put({"index" : i, "type" : "page", "url" : mission["url"], "header" : {}, "postdata" : {}})
            connectorNext = (connectorNext + 1) % connectorTotal
            cCounter += 1

        # start negotiation
        while aCounter or cCounter:
            for i,mission in enumerate(self.missions):
                if not aQueue[i][1].empty():
                    data = aQueue[i][1].get()
                    aCounter -= 1
                    for d in data:
                        if self.config["mode"] == "remote":
                            while not cServer.alives[connectorNext]:
                                connectorNext = (connectorNext + 1) % connectorTotal
                        cQueue[connectorNext][0].put(dict(d.items() + {"index" : i}.items()))
                        connectorNext = (connectorNext + 1) % connectorTotal
                        cCounter += 1
            for i in xrange(connectorTotal):
                if not cQueue[i][1].empty():
                    data = cQueue[i][1].get()
                    cCounter -= 1
                    if data["response"]:
                        index = data.pop("index")
                        aQueue[index][0].put(data)
                        aCounter += 1
