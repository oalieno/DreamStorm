import json
import socket

from lib.utils.utils import daemonThread,iterParse
from lib.utils.Log import Log

class Client:
    def __init__(self,q):
        self.q = q
        self.log = Log(__name__)
    def listen(self,ip,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip,port))
        self.log.info("Connect to " + ip + ':' + str(port))
        while True:
            data = ""
            while True:
                try:
                    data += sock.recv(4096)
                except socket.timeout:
                    break
            if data:
                for decoded in iterParse(data):
                    self.q[0].put(decoded)

            if not self.q[1].empty():
                data = self.q[1].get()
                sock.sendall(json.dumps(data))
