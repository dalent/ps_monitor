# -*- coding: utf-8 -*-
"""
Created by Jintao on 4/22/16.
parser logger moudule
"""

import logging
import os
import datetime


class loggerLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    pass


class loggerService:
    level = loggerLevel.DEBUG
    path = "./conf"
    logger = None
    fileHandler = None
    file = None

    def __init__(self, level=loggerLevel.DEBUG, path="./log"):
        self.level = level
        self.logger = logging.getLogger()
        self.path = path

    def checkAndMakeDir(self):
        if not os.path.exists(self.path):
            parentDir = os.path.dirname(self.path)
            if os.access(parentDir, os.W_OK):
                os.makedirs(self.path)
            else:
                return

    def checkHandle(self):
        if self.fileHandler is not None:
            return

        self.checkAndMakeDir()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        file = os.path.join(self.path, today + ".log")
        self.fileHandler = logging.FileHandler(file)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s')
        self.fileHandler.setFormatter(formatter)
        self.logger.addHandler(self.fileHandler)
        self.logger.setLevel(self.level)

    def check(self):
        self.checkHandle()

    def info(self, *msg):
        self.check()
        self.logger.info(msg)

    def debug(self, *msg):
        self.check()
        self.logger.debug(msg)

    def warning(self, *msg):
        self.check()
        self.logger.warning(msg)

    def error(self, *msg):
        self.check()
        self.logger.error(msg)

    pass


logger = loggerService(loggerLevel.DEBUG)


def info(*msg):
    logger.info(msg)


def debug(*msg):
    logger.debug(msg)


def warning(*msg):
    logger.warning(msg)


def error(*msg):
    logger.error(msg)
