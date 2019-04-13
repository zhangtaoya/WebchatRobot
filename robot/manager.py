# -*- coding:utf-8 -*-
import sys
from multiprocessing import Process
import os

import time
from lib import mongo
from lib import db
from lib import log
from service import wechat_service

from worker import robot_processor
while True:
    time.sleep(0.5)
    col_account = db.get_col_wechat_account_sync()
    doc = mongo.mongo_find_one(col_account, {'status': wechat_service.WECHAT_ACCOUNT_STATUS_INIT})
    if doc is False:
        log.error("db error for check init status wechat account, sleep 5s")
        time.sleep(5)
        continue

    if not doc:
        log.error("no wechat robot come in")
        continue
    mongo.mongo_update_one(col_account,
                           {'_id': doc['_id']},
                           {'$set': {'status': wechat_service.WECHAT_ACCOUNT_STATUS_WAIT_GEN_QR}})
    p = Process(target=robot_processor, args=(doc,))
    p.start()
    log.info("start new wechat robot")
