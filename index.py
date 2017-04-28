from base import BaseHandler
import tornado
from auth import dao as auth_dao
from auth import enums as auth_enums


class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')
