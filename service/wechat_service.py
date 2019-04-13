# -*- coding:utf-8 -*-
import sys
import time
from tornado import gen
from lib.db import *
from lib import motordb
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')

WECHAT_ACCOUNT_STATUS_INIT = 0
WECHAT_ACCOUNT_STATUS_WAIT_GEN_QR = 1
WECHAT_ACCOUNT_STATUS_WAIT_SCAN = 2
WECHAT_ACCOUNT_STATUS_DONE = 3
WECHAT_ACCOUNT_STATUS_WAIT_EXIT = 4
WECHAT_ACCOUNT_STATUS_DONE_EXIT = 5


@gen.coroutine
def new_user():
    col = get_col_wechat_account()
    doc = yield motordb.mongo_find_one(col, {'status': {'$lt': WECHAT_ACCOUNT_STATUS_DONE}})
    if doc is False:
        raise gen.Return({'ret': -1, 'data': {'msg': '后台数据库连接异常'}})
    if doc:
        raise gen.Return({'ret': -1, 'data': {'msg': '当前有号正在进行登陆'}})
    _id = str(uuid.uuid4())
    ts_call = int(time.time())
    doc = {'_id': _id, 'status': WECHAT_ACCOUNT_STATUS_INIT, 'ct': ts_call, 'ut': ts_call}
    ret = yield motordb.mongo_insert_one(col, doc)
    if not ret:
        raise gen.Return({'ret': -1, 'data': {'msg': '生成新数据失败'}})

    # max 20s
    qrcode = ''
    while time.time() < ts_call + 20:
        doc = yield motordb.mongo_find_one(col, {'_id': _id})
        if doc.get('status') == WECHAT_ACCOUNT_STATUS_WAIT_SCAN:
            qrcode = doc['qrcode']
            break
        time.sleep(0.5)

    raise gen.Return({'ret': 1, 'data': qrcode})

