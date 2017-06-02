# -*- coding: utf-8 -*-

from lib.utils import connect, tor_init


class Crawler:
    def __init__(self, q, tor):
        self.q = q
        if tor:
            tor_init()

    def run(self):
        while True:
            if not self.q[0].empty():
                package = self.q[0].get()
                result = connect(package)
                self.q[1].put(result)
