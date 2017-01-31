from bs4 import BeautifulSoup

class Agent:
    def __init__(self,mission):
        self.mission = mission
    def absolute(self,url):
        if url == None:
            return None
        if re.search("^https?://",url) == None:
            url = self.mission['domain'] + '/' + url.strip('/')
        url = url.partition('#')[0]
        if self.mission['range'] == "domain" and self.mission['domain'] not in url:
            url = None
        if self.mission['range'] == "subdomain" and self.mission['url'] not in url:
            url = None
        if self.mission['range'] == "page":
            url = None
        return url
    def generate(self,soup,url):
        pass
    def analyze(self,response):
        pass
    def run(self,tunnel):
        wholelist = []
        while True:
            if not tunnel.emptyin():
                data = tunnel.getin()
                analyze(data)
                soup = BeautifulSoup(data['response'],'lxml')
                urls = soup.find_all('a')
                tasks = []
                for url in urls:
                    url = self.absolute(url.get('href'))
                    if url and url not in wholelist:
                        wholelist.append(url)
                        tasks.append(generate(soup,url))
                tunnel.putout(tasks)
    def report(self):
        pass 
