# -*- coding: utf-8 -*-

import re

from bs4 import BeautifulSoup


class Pager:
    def __init__(self):
        self.urllist = {}

    @staticmethod
    def domain(url):
        if not url: return None
        head = url.find("//")
        tail = url[head + 2:].find("/")
        return url if tail == -1 else url[:head + 2 + tail]

    @staticmethod
    def absolute(domain, url, append):
        if not append: return None
        if re.search("^//", append) != None: return None
        # If don't have http or https prefix
        if re.search("^https?://", append) == None:
            # absolute url
            if append[0] == '/':
                append = domain + '/' + append.strip('/')
                # relative url
            else:
                append = url + '/' + append.strip('/')
        append = append.partition('#')[0].strip('/')
        if domain not in append: append = None
        return append

    def callback(self, package, page, headers):
        soup = BeautifulSoup(page, 'lxml')
        urls = soup.find_all('a')
        domain = self.domain(package["url"])
        self.urllist[domain] = self.urllist.get(domain, [])
        packages = []
        for url in urls:
            url = self.absolute(domain, package["url"], url.get('href'))
            if url and url not in self.urllist[domain]:
                self.urllist[domain].append(url)
                packages.append({
                    "url": url,
                    "headers": package["headers"],
                    "postdata": {}
                })
        return packages
