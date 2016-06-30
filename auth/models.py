# -*- coding: utf-8 -*-
import mongoengine as models
import datetime
from auth import enums


class User(models.Document):
    card_id = models.StringField(max_length=20, required=False)   # 工号
    username = models.StringField(max_length=20, required=False)  # 姓名
    password = models.StringField(required=True)  # 登陆密码
    age = models.IntField(required=False)    # 年龄
    sex = models.IntField(choices=enums.SEX_LIST, required=False)  # 性别
    department = models.StringField(max_length=30, required=False)  # 部门
    position = models.StringField(max_length=30, required=False)    # 岗位
    mobile = models.StringField(required=False)    # 电话
    emergency_contact = models.StringField(required=False)   # 紧急联系电话
    create_time = models.DateTimeField(default=datetime.datetime.now)  # 创建时间
    email = models.EmailField()    # 邮箱
    custom_attr = models.DictField()    # 定制属性
    perm = models.StringField(choices=enums.USER_PERMISSION_LIST, required=False)   # 权限
    status = models.IntField(choices=enums.USER_STATUS_LIST, default=enums.USER_STATUS_CHECK, required=True)  # 用户状态

    @property
    def oid(self):
        return str(self.id)

    meta = {
        'indexes': ['card_id', 'username']
    }


class Transaction(models.Document):
    user_id = models.StringField()     # 创建者
    ttype = models.IntField(choices=enums.TRANSACTION_TYPE_LIST)  # 事务类型
    create_time = models.DateTimeField(default=datetime.datetime.now)  # 事务的创建时间
    title = models.StringField()   # 标题
    content = models.StringField()    # 内容
    status = models.IntField(choices=enums.PROGRESS_LIST, default=enums.PROGRESS_CREATE)
    reason = models.StringField()    # 驳回原因
