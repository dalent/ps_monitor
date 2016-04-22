""" 
Created by Jintao on 4/21/16.
parser service conf or process conf
"""
from parser import confParser
class Config:
    pass

class ServiceListConfig:
    name=""
    config=[]
    def __init__(self,name,config):
        self.name=name
        #config split
        self.config=config.split(',')
    pass

class ProcessConfig:
    retryInterval=3
    failureRetries=10
    retryLimit=200
    environ=""
    name=""
    searchCmd=""
    startCmd=""
    autoRestart=1
    curRetries = 0
    def __init__(self,name,environ,searchCmd,startCmd,auto,retry,failureRetries,retryLimit):
        self.name=name
        self.environ=environ
        self.searchCmd=searchCmd
        self.startCmd = startCmd
        self.retry=retry
        self.failureRetries = failureRetries
        self.retryLimit = retryLimit
        self.autoRestart = auto
    pass

def parseServiceListConf(path):
    parser = confParser()
    parserResult = parser.parser(path)
    if parserResult is None:
        return None
    services=[]
    for sectionName,values in parserResult:
        if sectionName != "":
            services=append(ServiceListConfig(sectionName,values["CONFIG"]))

parseServiceListConf("service.conf")

    




