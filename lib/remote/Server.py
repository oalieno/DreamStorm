import json
import socket
import threading

from lib.utils.Log import Log
from lib.utils.Utils import daemonThread,iterParse

class Server:
    def __init__(self):
        self.log = Log(__name__)
        self.q = {}
        self.alives = {}

    def addTunnel(self,q,name):
        self.q[name] = q
        self.alives[name] = False

    def listen(self,ip,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((ip,port))
        sock.listen(len(self.q))

        while True:
            client,address = sock.accept()
            name = ""
            for key,value in self.alives.iteritems():
                if not value:
                    name = key
                    break
            self.alives[name] = True
            daemonThread(self.talkToClient,(client,address,name))

    def talkToClient(self,client,address,name):
        self.log.info("Connect to " + address[0] + ":" + str(address[1]))
        client.settimeout(1)
        while True:
            data = ""
            while True:
                try:
                    data += client.recv(4096)
                except socket.timeout:
                    break
            if data:
                for decoded in iterParse(data):
                    self.q[name][1].put(decoded)

            if not self.q[name][0].empty():
                client.sendall(json.dumps(self.q[name][0].get()))          
