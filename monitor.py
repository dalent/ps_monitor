# -*- coding: utf-8 -*-
"""
Created by Jintao on 4/21/16.
main file
"""


import config
import process
import time


class Monitor:
    confPath = ''
    processConfs = []
    processes = []

    def __init__(self, confPath='conf/'):
        self.confPath = confPath
        self.initConf()
        self.parseProcesses()

    def initConf(self):
        self.processConfs = config.parseProcessDir(self.confPath)

    def parseProcesses(self):
        for conf in self.processConfs:
            self.processes.append(process.Process(conf))

    def checkProcess(self):
        for proc in self.processes:
            proc.checkProcess()

    pass

monitor = None

if __name__ == '__main__':
    global monitor
    monitor = Monitor('./conf')
    while True:
        monitor.checkProcess()
        time.sleep(1)
