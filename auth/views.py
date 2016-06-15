# -*- coding: utf-8 -*-
from base import BaseHandler
from common.utils import md5
from auth import dao
import json


class RegisterHandler(BaseHandler):
    def get(self):
        self.render('auth/register.html')

    def post(self):
        card_id = self.get_argument('card_id', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        password1 = self.get_argument('password1', '')
        age = self.get_argument('age', '')
        sex = int(self.get_argument('sex', 0))
        department = self.get_argument('department', '')
        position = self.get_argument('position', '')
        mobile = self.get_argument('mobile', '')
        emergency_contact = self.get_argument('emergency_contact', '')
        email = self.get_argument('email', '')

        if password != password1:
            self.write('password input do not match twice')
            return

        user = dao.get_user(username=username)
        if user:
            self.write('user already exist')
            return

        dao.add_user(card_id, username, password, age, sex, department, position, mobile, emergency_contact, email)
        self.redirect('/login/')


class LoginHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        err_msg = ''
        username = ''
        if not user:
            self.render('auth/login.html', err_msg=err_msg, username=username)
        else:
            self.redirect('/')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        user = dao.get_user(username)
        err_msg = ''
        if not user or user.password != md5(password):
            err_msg = 'username does not match password'
            self.render('auth/login.html', err_msg=err_msg, username=username)
            return

        self.set_cookie('user', user.username)
        self.redirect('/')


class JsLoginHandler(BaseHandler):
    """课后练习，在首页上家一个按钮，点击的时候弹出一个登陆框"""
    def get(self):
        user = self.get_current_user()
        err_msg = ''
        if not user:
            self.render('auth/jslogin.html', err_msg=err_msg)
        else:
            self.redirect('/')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        print username, password

        user = dao.get_user(username)
        if not user or user.password != md5(password):
            self.write(json.dumps({'status': 'fail'}))
            return

        self.set_cookie('user', '888')
        self.write(json.dumps({'status': 'ok'}))

    def check_xsrf_cookie(self):
        return


class LogoutHandler(BaseHandler):
    def get(self):
        pass
