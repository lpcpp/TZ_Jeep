# -*- coding: utf-8 -*-
from base import AdminBaseHandler
from common.utils import md5
from admin import dao
from auth import dao as auth_dao
from auth import enums as auth_enums
import json


class LoginHandler(AdminBaseHandler):
    def get(self):
        user = self.get_current_user()
        err_msg = ''
        username = ''
        if not user:
            self.render('admin/login.html', err_msg=err_msg, username=username)
        else:
            self.redirect('/admin/')

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')

        admin_user = dao.get_admin_user(username)
        err_msg = ''
        if not admin_user or admin_user.password != md5(password):
            err_msg = 'username does not match password'
            self.render('admin/login.html', err_msg=err_msg, username=username)
            return

        self.set_secure_cookie('admin_user', admin_user.username)
        self.redirect('/admin/')


class LogoutHandler(AdminBaseHandler):
    def get(self):
        pass


class AdminHandler(AdminBaseHandler):
    def get(self):
        self.render('admin/admin.html')


class AdminUserListHandler(AdminBaseHandler):
    def get(self):
        sort = self.get_argument('sort', '-created')
        search = self.get_argument('search', '')
        search_value = self.get_argument('search_value', '')
        admin_user = self.get_secure_cookie('admin_user')
        if not admin_user:
            self.redirect('/admin/login/')
            return
        user_list = auth_dao.get_user_list().order_by(sort)
        if search == 'name':
            user_list = user_list.filter(name=search_value)
        elif search == 'card_id':
            user_list = user_list.filter(card_id=search_value)
        elif search == 'mobile':
            user_list = user_list.filter(mobile=search_value)
        elif search == 'email':
            user_list = user_list.filter(email=search_value)
        elif search == 'perm':
            user_list = user_list.filter(perm=search_value)
        elif search == 'status':
            user_list = user_list.filter(status=search_value)
        elif search == 'department':
            user_list = user_list.filter(department=search_value)
        elif search == 'position':
            user_list = user_list.filter(position=search_value)

        user_status_dict = auth_enums.USER_STATUS_DICT
        self.render('admin/user_list.html', user_list=user_list, user_status_dict=user_status_dict)


class AddUserHandler(AdminBaseHandler):
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
        perm_list = auth_enums.USER_PERMISSION_LIST
        params = locals()
        params.pop('self')

        self.render('admin/add_user.html', **params)

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
        perm = self.get_argument('perm', '')

        if not (username and password and password1 and age and sex and department and position and mobile and emergency_contact and email and perm):
            err_msg = 'lack of argument'
            params = locals()
            params.pop('self')
            self.render('admin/add_user.html', **params)
            return

        if password != password1:
            err_msg = 'password input do not match twice'
            params = locals()
            params.pop('self')
            self.render('admin/add_user.html', **params)
            return

        user = auth_dao.get_user(username=username)
        if user:
            err_msg = 'user already exist'
            params = locals()
            params.pop('self')
            self.render('auth/register.html', **params)
            return

        auth_dao.add_user(username, password, age, sex, department, position, mobile, emergency_contact, email, perm=perm)
        self.redirect('/admin/')


class CheckUserHandler(AdminBaseHandler):
    def post(self):
        check_user = self.get_argument('check_user', '')
        card_id = self.get_argument('card_id', '')
        if check_user == 'pass':
            status = auth_enums.USER_STATUS_NORMAL
        elif check_user == 'active':
            status = auth_enums.USER_STATUS_NORMAL
        elif check_user == 'nopass':
            status = auth_enums.USER_STATUS_NOPASS
        elif check_user == 'forbid':
            status = auth_enums.USER_STATUS_FORBID
        elif check_user == 'delete':
            status = auth_enums.USER_STATUS_DELETE
        else:
            self.write(json.dumps({'status': 'fail', 'err_msg': 'args mistake'}))
            return

        auth_dao.update_user_by_card_id(card_id, {'status': status})
        self.write(json.dumps({'status': 'ok'}))
        return

    def check_xsrf_cookie(self):
        return
