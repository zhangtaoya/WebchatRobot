#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
import os.path
import datetime
from config import config

logger = None


def init_logger(service, level=logging.DEBUG, console=False):
    global logger
    if logger:
        return logger
    logger = logging.getLogger(service)
    logger.setLevel(level)

    filefmt = os.path.join(config.LOG_PATH, service, service + "-%Y-%m-%d.log")
    handler = ServiceLoggerHandler(filefmt)
    fmt = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s:%(lineno)s --> %(message)s')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    if console:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger


def logout(level, infos):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lo = '%s - %s -->' % (level, now)
    lo = '%s %s' % (lo, infos)
    print (lo)


def split_msg(message):
    if len(message) > 4096:
        message = message[:4096]
    return message


def debug(message):
    message = split_msg(message)
    if logger:
        logger.debug(message)
    else:
        logout('DEBUG', message)


def info(message):
    message = split_msg(message)
    if logger:
        logger.info(message)
    else:
        logout('INFO', message)


def warn(message):
    message = split_msg(message)
    if logger:
        logger.warn(message)
    else:
        logout('WARN', message)


def error(message):
    message = split_msg(message)
    if logger:
        logger.error(message)
    else:
        logout('ERROR', message)


def critical(message):
    message = split_msg(message)
    if logger:
        logger.critical(message)
    else:
        logout('CRITICAL', message)


class ServiceLoggerHandler(logging.Handler):
    def __init__(self, filefmt=None):
        self.filefmt = filefmt
        if filefmt is None:
            self.filefmt = os.path.join("logs", "%Y-%m-%d.log")
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        fpath = datetime.datetime.now().strftime(self.filefmt)
        fdir = os.path.dirname(fpath)
        try:
            if not os.path.exists(fdir):
                os.makedirs(fdir)
        except Exception:
            pass

        try:
            f = open(fpath, 'a')
            f.write(msg)
            f.write("\n")
            f.flush()
            f.close()
        except Exception:
            pass
