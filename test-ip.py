import socks
import socket
import urllib

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,"127.0.0.1",9050,True)
socket.socket = socks.socksocket

print urllib.urlopen("http://jsonip.com").read()

