import Queue

from lib.remote.Server import Server
from lib.unit.Pager import Pager
from lib.unit.Fuzzer import Fuzzer
from lib.unit.Connector import Connector
from lib.utils.Utils import daemonThread

class Manager:
    def __init__(self,config,missions):
        self.config = config
        self.missions = missions
    def run(self):
        '''
        Connector tunnel in : {"index" : integer, "url" : string, "header" : dictionary, "postdata" : dictionary}
        Connector tunnel out : {"index" : integet, "url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
        '''

        '''
        Pager tunnel in : {"url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
        Pager tunnel out : [{"url" : string, "header" : dictionary, "postdata" : dictionary},...]
        '''
        
        '''
        Fuzzer tunnel in : {"url" : string, "header" : dictionary, "postdata" : dictionary, "response" : string}
        Fuzzer tunnel out : [{"url" : string, "header" : dictionary, "postdata" : dictionary},...]
        '''

        # queue-in and queue-out
        pQueue = [(Queue.Queue(),Queue.Queue()) for i in xrange(len(self.missions))]
        fQueue = [(Queue.Queue(),Queue.Queue()) for i in xrange(len(self.missions))]
        cQueue = [(Queue.Queue(),Queue.Queue()) for i in xrange(self.config["Connector-threads"])]

        # send config and missions
        for i,mission in enumerate(self.missions):
            pQueue[i][0].put(mission)
            fQueue[i][0].put(mission)
        for i in xrange(self.config["Connector-threads"]):
            cQueue[i][0].put(self.config)

        # start pager and fuzzer locally
        for i,mission in enumerate(self.missions):
            p = Pager(pQueue[i])
            f = Fuzzer(fQueue[i])
            daemonThread(p.run)
            daemonThread(f.run)

        if self.config["mode"] == "local":
            # start connectors locally
            for i in xrange(self.config["Connector-threads"]):
                c = Connector(cQueue[i])
                daemonThread(c.run)
        else:
            # start connectors remotely
            cServer = Server()
            for i in xrange(self.config["Connector-threads"]):
                cServer.addTunnel(cQueue[i],"Connector" + str(i))
            daemonThread(cServer.listen,(self.config["ip"],self.config["port"]))

        pCounter = 0
        fCounter = 0
        cCounter = 0

        connectorNext = 0
        connectorTotal = self.config["Connector-threads"]

        # put initial tasks
        for i,mission in enumerate(self.missions):
            if self.config["mode"] == "remote":
                while not cServer.alives["Connector" + str(connectorNext)]:
                    connectorNext = (connectorNext + 1) % connectorTotal
            cQueue[connectorNext][0].put({"index" : i, "origin" : "Pager", "url" : mission["url"], "header" : {}, "postdata" : {}})
            connectorNext = (connectorNext + 1) % connectorTotal
            cCounter += 1

        # start negotiation
        while pCounter or fCounter or cCounter:
            for i in xrange(len(self.missions)):
                if not pQueue[i][1].empty():
                    data = pQueue[i][1].get()
                    pCounter -= 1
                    for d in data:
                        if self.config["mode"] == "remote":
                            while not cServer.alives["Connector" + str(connectorNext)]:
                                connectorNext = (connectorNext + 1) % connectorTotal
                        cQueue[connectorNext][0].put(dict(d.items() + {"index" : i,"origin" : "Pager"}.items()))
                        connectorNext = (connectorNext + 1) % connectorTotal
                        cCounter += 1
                if not fQueue[i][1].empty():
                    data = fQueue[i][1].get()
                    fCounter -= 1
                    for d in data:
                        if self.config["mode"] == "remote":
                            while not cServer.alives[connectorNext]:
                                connectorNext = (connectorNext + 1) % connectorTotal
                        cQueue[connectorNext][0].put(dict(d.items() + {"index" : i,"origin" : "Fuzzer"}.items()))
                        connectorNext = (connectorNext + 1) % connectorTotal
                        cCounter += 1
            for i in xrange(connectorTotal):
                if not cQueue[i][1].empty():
                    data = cQueue[i][1].get()
                    cCounter -= 1
                    if data["response"]:
                        pQueue[data["index"]][0].put(data)
                        pCounter += 1
                        fQueue[data["index"]][0].put(data)
                        fCounter += 1
