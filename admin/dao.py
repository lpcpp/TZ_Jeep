from admin.models import AdminUser
from common.utils import md5


def add_user(username, password):
    admin_user = AdminUser(
        username=username,
        password=md5(password),
    )

    admin_user.save()


def get_admin_user(username):
    try:
        admin_user = AdminUser.objects.get(username=username)
    except:
        admin_user = None

    return admin_user
