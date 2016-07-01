# -*- coding: utf-8 -*-
from base import BaseHandler
from common.utils import md5
from auth import dao
from auth import enums
import json
import tornado.web


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

        print email

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

        print '8888'
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


class InfoHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        print user
        user = dao.get_user(user)
        self.render('auth/user_info.html', user=user)

    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        user = dao.get_user(user)
        mobile = self.get_argument('mobile')
        emergency_contact = self.get_argument('emergency_contact')

        dao.update_user_by_card_id(user.card_id, {'mobile': mobile, 'emergency_contact': emergency_contact})
        self.redirect('/member/')


class TransactionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, action):
        if action == 'list':
            user = self.get_current_user()
            user_id = dao.get_user(user).oid
            transaction_list = dao.get_transaction_list_by_user_id(user_id)
            self.render('auth/transaction.html', transaction_list=transaction_list)
        elif action == 'add':
            self.render('auth/add_transaction.html')

    @tornado.web.authenticated
    def post(self, action):
        if action == 'update':
            transaction_id = self.get_argument('transaction_id', '')
            title = self.get_argument('title', '')
            content = self.get_argument('content', '')
            status = 1
            attr = {'title': title, 'content': content, 'status': status}
            dao.update_transaction_by_id(transaction_id, attr)
            self.write(json.dumps({'status': 'ok'}))
        else:
            user = self.get_current_user()
            user_id = dao.get_user(user).oid
            ttype = int(self.get_argument('ttype'))
            title = self.get_argument('title')
            content = self.get_argument('content')
            dao.add_transaction(user_id, ttype, title, content)
            self.redirect('/auth/transaction/list/')

    def check_xsrf_cookie(self):
        return


class ReviewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        user = dao.get_user(user)
        user_id = user.oid
        print 'name:', user.to_json()
        print 'perm:', user.perm
        if user.perm == enums.ACADEMY:
            status = 1
        if user.perm == enums.BUSINESS:
            status = 2
        if user.perm == enums.CLUSTER:
            status = 3
        transaction_list = dao.get_transaction_list_by_status(status)
        result = []
        for transaction in transaction_list:
            tmp = {}
            user = dao.get_user_by_user_id(transaction.user_id)
            tmp['id'] = str(transaction.id)
            tmp['user'] = user.username
            tmp['ttype'] = transaction.ttype
            tmp['title'] = transaction.title
            tmp['content'] = transaction.content
            result.append(tmp)
        self.render('auth/review_list.html', transaction_list=result)

    def post(self):
        transaction_id = self.get_argument('transaction_id', '')
        action = self.get_argument('action', '')
        reason = self.get_argument('reason', '')

        if action == 'pass':
            dao.update_transaction_by_id(transaction_id, {'status': 1})
        if action == 'nopass':
            dao.update_transaction_by_id(transaction_id, {'status': 0, 'reason': reason})

        print '1111', action, transaction_id, reason
        self.write(json.dumps({'status': 'ok'}))

    def check_xsrf_cookie(self):
        return
