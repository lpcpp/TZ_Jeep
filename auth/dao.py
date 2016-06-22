from auth.models import User
from common.utils import md5, make_card_id
from auth import enums as auth_enums


def add_user(username, password, age, sex, department, position, mobile, emergency_contact, email, perm=None):
    if perm in [auth_enums.ACADEMY, auth_enums.BUSINESS, auth_enums.CLUSTER]:
        status = auth_enums.USER_STATUS_NORMAL
    else:
        status = auth_enums.USER_STATUS_CHECK
    card_id = str(make_card_id())
    user = User(
        card_id=card_id,
        username=username,
        password=md5(password),
        age=age,
        sex=sex,
        department=department,
        position=position,
        mobile=mobile,
        emergency_contact=emergency_contact,
        email=email,
        perm=perm,
        status=status
    )

    user.save()


def get_user(username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    return user


def get_user_by_card_id(card_id):
    try:
        user = User.objects.get(card_id=card_id)
    except:
        user = None

    return user


def get_user_list():
    user_list = User.objects.all()
    return user_list


def update_user_by_card_id(card_id, kwargs):
    user = get_user_by_card_id(card_id)
    for key, value in kwargs.iteritems():
        user[key] = value

    user.save()

    return user
