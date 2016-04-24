# -*- coding: utf-8 -*-
"""
Created by Jintao on 4/21/16.
parser service conf or process conf
"""
from parser import confParser
import os
import glob


class Config:
    pass


class ServiceListConfig:
    name = ""
    confi = []

    def __init__(self, name, config):
        self.name = name
# config split
        self.config = config.split(',')
    pass


"""
分析process的配置文件，包含几个部分程序名字，程序启动命令，查询命令，是不是要自动重启等。
"""


class ProcessConfig:
    retryInterval = 3
    failureRetries = 10
    retryLimit = 200
    environ = ""
    name = ""
    searchCmd = ""
    searchStr = ""
    startCmd = ""
    user = ""
    directory = ""
    autoRestart = 1

    def __init__(self, name='', environ='', user='', searchCmd='',
                 directory='', startCmd='', auto=1,
                 failureRetries=3, retryLimit=200):
        self.name = name
        self.environ = environ
        self.searchCmd = searchCmd
        self.user = user
        self.directory = directory
        self.startCmd = startCmd
        self.failureRetries = failureRetries
        self.retryLimit = retryLimit
        self.autoRestart = auto

    def checkValid(self):
        if self.name == "" or self.startCmd == "" or \
           (self.searchStr == "" and self.searchCmd == ""):
            return False
        return True

    def __str__(self):
        return "retryInterval:" + str(self.retryInterval) + " name:" + \
               self.name + " startcmd:" + self.startCmd + " search:" + \
               self.searchCmd + 'failure retry:' + \
               str(self.failureRetries)

    def __repr__(self):
        return self.__str__()
    pass


def parseServiceListConf(path):
    parser = confParser()
    parserResult = parser.parse(path)
    services = []
    if parserResult is None:
        return services

    for sectionName, values in parserResult.items():
        if sectionName != "":
            services.append(ServiceListConfig(sectionName,
                                              values["LOG_LEVEL_STRING"]))
    return services


def parseProcessDir(dirname):
    if not os.path.isdir(dirname):
        return None

    files = glob.glob(os.path.join(dirname, '*.conf'))
    processes = []
    for file in files:
        process = parseProcessConf(file)
        if process is not None:
            processes.append(process)
    return processes


def parseProcessConf(path):
    parser = confParser()
    parseResult = parser.parse(path)
    if parseResult is None:
        return None

    for sectionName, values in parseResult.items():
        if sectionName == "":
            tmpProcess = ProcessConfig()
            for k, v in values.items():
                if k == 'name':
                    tmpProcess.name = v
                elif k == 'search_str':
                    tmpProcess.searchStr = v
                elif k == 'start_command':
                    tmpProcess.startCmd = v
                elif k == 'user':
                    tmpProcess.user = v
                elif k == 'auto_restart':
                    tmpProcess.autoRestart = v
                elif k == 'retries':
                    tmpProcess.failureRetries = int(v)
                elif k == 'search_command':
                    tmpProcess.searchCmd = v
                elif k == 'retry_interval':
                    tmpProcess.retryInterval = int(v)
                elif k == 'directory':
                    tmpProcess.directory = v
                elif k == 'total_retry_times':
                    tmpProcess.retryLimit = int(v)
                elif k == 'directory':
                    tmpProcess.directory = v

            if tmpProcess.checkValid():
                return tmpProcess

    return None
