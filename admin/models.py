import mongoengine as models
import datetime
from admin import enums


class AdminUser(models.Document):
    username = models.StringField(max_length=20, required=False)
    department = models.StringField(max_length=30, required=False)
    mobile = models.StringField(required=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    perm = models.StringField(choices=enums.ADMIN_USER_PERMISSION_LIST)
    custom_attr = models.DictField()
