# -*- coding:utf-8 -*-

"""
Created by Jintao on 4/21/16.
parser service conf or process conf
"""

import logger
import commands
import os


class Process:
    options = None
    pids = []
    curFailedRetry = 0
    curTotalTry = 0

    def __init__(self, conf):
        self.options = conf

    def checkProcess(self):
        if self.curFailedRetry > self.options.failureRetries:
            logger.info(self.options,
                        ":fail times reach threshold, not monitor")
        if len(self.pids) == 0:
            self.getPid()
        if len(self.pids) == 0:
            self.start()
        return
        pass

    def start(self):
        if self.curFailedRetry > self.options.failureRetries:
            logger.error("failed retry reach limit", self)
            return
        if self.curTotalTry > 200:
            logger.error("total retry reach limit:", self)
            return
        if self.options.startCmd == "":
            logger.error("it should never reach here:", self)
            return

        cmd = 'nohup sh -c \"%s\" &'\
              % (self.options.startCmd)

        # cmd = '"\"nohup ls &\""'
        print cmd
        logger.debug(self.options.name, " start:", cmd, self)
        """status, output = commands.getstatusoutput(cmd)
        print output
        if status != 0:
            logger.error("start process failed:", status, self)
            return
        """
        status = os.system(cmd)
        if status != 0:
            logger.error("start process failed:", status, self)
            return

        self.getPid()
        if len(self.pids) == 0:
            self.curFailedRetry += 1
        else:
            self.curFailedRetry = 0

        self.curTotalTry += 1
        pass

    def getPid(self):
        cmd = self.options.searchCmd
        if cmd == "":
            if self.options.searchStr != "":
                if self.options.user != "":
                    cmd = "ps -U %s -u %s -ww u|grep -v grep" \
                          % (self.options.user, self.options.user)
                else:
                    logger.error("user is none:", self.options)
                    return
                greps = self.options.searchStr.split(',')
                subGrep = ""
                for grep in greps:
                    subGrep = '%s | grep %s' % (subGrep, grep)
                if subGrep == '':
                    # 没有subgrep 不执行监控
                    logger.error("searchStr error:", self.options)
                    return
                cmd = '%s %s' % (cmd, subGrep)
        if cmd == "":
            logger.error("search cmd wrong:", self.options)
            return

        # data = subprocess.Popen(cmd, stdout = subprocess.PIPE, shell=True)
        (status, output) = commands.getstatusoutput(cmd)
        if status != 0:
            logger.info("get process id failed:",
                        status, output, self.options)
        lines = output.split('\n')
        pids = []

        for line in lines:
            sections = line.strip().split()
            if len(sections) > 2:
                if not sections[1].isdigit():
                    continue

                pid = int(sections[1])
                if pid != 0:
                    pids.append(pid)

        self.pids = pids
        logger.info(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.options.__repr__() + " pid:" + self.pids.__str__()

    pass
