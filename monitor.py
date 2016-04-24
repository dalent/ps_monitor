# -*- coding: utf-8 -*-
"""
Created by Jintao on 4/21/16.
main file
"""


import logger
import config
import process


class monitor:
    confPath = ''
    processConfs = []
    processes = []

    def __init__(self, confPath='conf/'):
        self.confPath = confPath
        self.initConf()
        self.parseProcesses()

    def initConf(self):
        self.processConfs = config.parseProcessConf(self.confPath)

    def parseProcesses(self):
        if self.confs is None:
            logger.info("no conf file ignore")
            return
        for conf in self.processConfs:
            self.processes.append(process.Process(conf))

    pass


if __name__ == '__main__':
    confs = config.parseProcessDir('conf')
    logger.logger.info(confs)
    processes = []
    for conf in confs:
        processes.append(process.Process(conf))
    for proc in processes:
        proc.checkProcess()
