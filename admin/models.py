import mongoengine as models
import datetime


class AdminUser(models.Document):
    username = models.StringField(max_length=20, required=True)
    password = models.StringField(required=True)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    custom_attr = models.DictField()
