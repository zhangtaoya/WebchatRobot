# -*- coding:utf-8 -*-
import sys
import base64, time
from lib.ItChat import itchat
from lib import log
from lib import mongo, db
from service import wechat_service


def robot_processor(param):
    _id = param['_id']
    weChatInstance = itchat.new_instance()

    def qr_callback(uuid, status, qrcode):
        log.info("qr_callback for _id:%s" % _id)
        col_account = db.get_col_wechat_account_sync()
        doc = mongo.mongo_find_one(col_account, {'_id': _id})
        if not doc:
            log.error("qr_callback@check record _id:%s failed" % _id)
            return

        data = base64.b64encode(qrcode)
        ts_now = int(time.time())
        ret = mongo.mongo_update_one(col_account, {'_id': _id},
                                     {'$set': {'data': data, 'ut': ts_now,
                                               'status': wechat_service.WECHAT_ACCOUNT_STATUS_WAIT_SCAN}})
        if not ret:
            log.error("qr_callback@update _id:%s data failed" % _id)
        log.info("qr_callback@update _id:%s data succeed" % _id)

    def login_process(_id):
        weChatInstance.auto_login(qrCallback=qr_callback)
        log.info("login for _id:%s complete" % _id)
        col_account = db.get_col_wechat_account_sync()
        doc = mongo.mongo_find_one(col_account, {'_id': _id})
        if not doc:
            log.error("login process for _id:%s doc check failed, now logout" % _id)
            weChatInstance.logout()

        ret = mongo.mongo_update_one(col_account, {'_id': _id},
                                     {'$set': {'status': wechat_service.WECHAT_ACCOUNT_STATUS_DONE}})
        if not ret:
            log.error("login process for update done status failed: %s, now logout" % _id)
            weChatInstance.logout()

    def log_out(_id):
        weChatInstance.logout()
        log.info("user logout done, now update db status")
        col_account = db.get_col_wechat_account_sync()
        ret = mongo.mongo_update_one(col_account, {'_id': _id},
                                     {'$set': {'status': wechat_service.WECHAT_ACCOUNT_STATUS_DONE_EXIT}})
        if not ret:
            log.error("log_out update db status failed")

    def work():
        log.info("task idle, try one work")
        return

    while True:
        time.sleep(0.5)
        col_account = db.get_col_wechat_account_sync()
        doc = mongo.mongo_find_one(col_account, {'_id': _id})
        if not doc:
            log.error("check _id:%s doc check failed, now exit" % _id)
            sys.exit(0)
        status = doc['status']

        if status == wechat_service.WECHAT_ACCOUNT_STATUS_WAIT_GEN_QR:
            login_process(_id)
        elif status == wechat_service.WECHAT_ACCOUNT_STATUS_WAIT_EXIT:
            log_out(_id)
            sys.exit(0)
        else:
            work()
