# -*- coding: utf-8 -*-
"""
Created by Jintao on 4/21/16.
parser service conf or process conf
"""
from parser import confParser


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


class ProcessConfig:
    retryInterval = 3
    failureRetries = 10
    retryLimit = 200
    environ = ""
    name = ""
    searchCmd = ""
    startCmd = ""
    autoRestart = 1
    curRetries = 0

    def __init__(self, name, environ, searchCmd,
                 startCmd, auto=1, failureRetries=3, retryLimit=200):
        self.name = name
        self.environ = environ
        self.searchCmd = searchCmd
        self.startCmd = startCmd
        self.failureRetries = failureRetries
        self.retryLimit = retryLimit
        self.autoRestart = auto
    pass


def parseServiceListConf(path):
    parser = confParser()
    parserResult = parser.parse(path)
    services = []
    if parserResult is None:
        return services

    for sectionName, values in parserResult:
        if sectionName != "":
            services.append(ServiceListConfig(sectionName,
                                              values["LOG_LEVEL_STRING"]))


def parseProcessConf(path):
    parser = confParser()
    parseResult = parser.parse(path)
    process = []
    if parseResult is None:
        return process

    for sectionName, values in parseResult:
        if sectionName == "":
            process.append(ProcessConfig())


