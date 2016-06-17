# -*- coding: utf-8 -*-
from base import BaseHandler
from common.utils import md5
from auth import dao
from auth import enums
import json


class RegisterHandler(BaseHandler):
    def get(self):
        err_msg = ''
        username = ''
        age = ''
        sex = ''
        department = ''
        position = ''
        mobile = ''
        emergency_contact = ''
        email = ''
        params = locals()
        params.pop('self')
        print params

        self.render('auth/register.html', **params)

    def post(self):
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

        if not (username and password and password1 and age and sex and department and position and mobile and emergency_contact and email):
            err_msg = 'lack of argument'
            params = locals()
            params.pop('self')
            self.render('auth/register.html', **params)
            return

        if password != password1:
            err_msg = 'password input do not match twice'
            params = locals()
            params.pop('self')
            self.render('auth/register.html', **params)
            return

        user = dao.get_user(username=username)
        if user:
            err_msg = 'user already exist'
            params = locals()
            params.pop('self')
            self.render('auth/register.html', **params)
            return

        dao.add_user(username, password, age, sex, department, position, mobile, emergency_contact, email)
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
        if not user.status == enums.USER_STATUS_NORMAL:
            self.write('your acccount is checking')
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
