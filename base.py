# -*- coding: utf-8 -*-

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_cookie('user')
        if user:
            return user


class AdminBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        admin_user = self.get_secure_cookie('admin_user')
        if admin_user:
            return admin_user
