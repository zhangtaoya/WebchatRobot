#!/usr/bin/env python
# coding:utf-8
import base64

from service import my_service, wechat_service
from base_handler import BaseHandler


class IndexHandler(BaseHandler):
    def get(self):
        ret = my_service.service_hello(0)
        self.render("../public/index.html")


class LSJHandler(BaseHandler):
    def post(self):
        data = open('./public/test.png').read()
        self.write(data)
        self.set_header("Content-type", "image/png")

    def get(self):
        data = open('./public/test.png').read()
        self.write(data)
        self.set_header("Content-type", "image/png")


class WechatLoginHandler(BaseHandler):
    def get(self):
        ret = yield wechat_service.new_user()
        if ret.get('ret') != 1:
            self.write(ret)
            return
        data = ret['data']
        data_bin = base64.b64decode(data)
        self.write(data_bin)
        self.set_header("Content-type", "image/png")
