# -*- coding: utf-8 -*-

import Queue
import random

from Crawler import Crawler
from lib.utils import daemonThread


class DreamStorm:
    """ Main Engine of DreamStorm
    It's just awesome...
    """

    def __init__(self, threads, tor=False):
        self.counter = 0
        self.threads = threads
        self.tor = tor
        self.q = (Queue.Queue(), Queue.Queue())
        self.qq = []
        for i in xrange(self.threads):
            self.qq.append((Queue.Queue(), Queue.Queue()))
            c = Crawler(self.qq[-1], self.tor)
            daemonThread(c.run)

    def put(self, url, headers=None, postdata=None):
        headers = headers or {}
        postdata = postdata or {}
        url_list = []
        if type(url) in (dict, str, unicode): url_list = [url]
        elif type(url) in (list, ): url_list = url
        else: raise
        for url_item in url_list:
            _url = ""
            _headers = headers
            _postdata = postdata
            if type(url_item) in (str, unicode): _url = url_item
            elif type(url_item) in (dict, ):
                _url = url_item.get("url", _url)
                _headers = url_item.get("headers", _headers)
                _postdata = url_item.get("postdata", _postdata)
            else:
                raise
            self.counter += 1
            self.q[0].put({
                "url": _url,
                "headers": _headers,
                "postdata": _postdata
            })

    def run(self, *callbacks):
        while self.counter:
            if not self.q[0].empty():
                rand = random.randint(0, self.threads - 1)
                self.qq[rand][0].put(self.q[0].get())
            for q in self.qq:
                if not q[1].empty():
                    package = q[1].get()
                    for callback in callbacks:
                        packages = callback(package[0], package[1], package[2])
                        if packages: self.put(packages)
                    self.counter -= 1
