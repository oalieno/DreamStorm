import json
import socket
import threading

from lib.utils.utils import daemonThread,iterParse
from lib.utils.Log import Log

class Server:
    def __init__(self):
        self.log = Log(__name__)
        self.q = []
        self.alives = []

    def addTunnel(self,q):
        self.q.append(q)
        self.alives.append(False)

    def listen(self,ip,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((ip,port))
        sock.listen(len(self.q))

        while True:
            client,address = sock.accept()
            for i,alive in enumerate(self.alives):
                if not alive:
                    self.alives[i] = True
                    daemonThread(self.talkToClient,(client,address,self.q[i]))
                    break

    def talkToClient(self,client,address,q):
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
                    q[1].put(decoded)

            if not q[0].empty():
                client.sendall(json.dumps(q[0].get()))
