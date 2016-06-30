from base import BaseHandler
import tornado
from auth import dao as auth_dao
from auth import enums as auth_enums


class IndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        user = auth_dao.get_user(user)
        if user.status != auth_enums.USER_STATUS_NORMAL:
            self.write('your account is checking')
            return

        perm = ''
        if user.perm == auth_enums.ACADEMY:
            perm = auth_enums.ACADEMY

        self.render('index.html', perm=perm)
