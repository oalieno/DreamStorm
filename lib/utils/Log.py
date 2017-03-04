import sys
import logging

from lib.utils.Color import Color

class Log:
    def __init__(self,name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        self.logger.addHandler(self.handler)
    def debug(self,text):
        self.logger.debug(Color.bold+Color.aquamarine+"\t"+text+Color.normal)
    def info(self,text):
        self.logger.info(Color.bold+Color.green+"\t\t"+text+Color.normal)
    def info2(self,text):
        self.logger.info(Color.green+"\t\t"+text+Color.normal)
    def info3(self,text):
        self.logger.info("\t\t"+text)
    def warning(self,text):
        self.logger.warning(Color.bold+Color.yellow+"\t"+text+Color.normal)
    def error(self,text):
        self.logger.error(Color.bold+Color.red+"\t"+text+Color.normal)
        #self.logger.error(Color.bold+Color.red+"\t"+"type -h to see the usage"+Color.normal)
        sys.exit(0)
