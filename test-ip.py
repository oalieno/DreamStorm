#!/usr/bin/python
import socks
import socket

from stem import Signal
from stem.control import Controller

from lib.core import connect

controller = Controller.from_port(port = 9051)

def newIdentity():
    controller.authenticate("YourPassword")
    controller.signal(Signal.NEWNYM)

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
socket.socket = socks.socksocket

print connect("http://jsonip.com",{},{})
