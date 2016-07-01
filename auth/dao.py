from auth.models import User, Transaction
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


def get_user_by_user_id(user_id):
    try:
        user = User.objects.get(id=user_id)
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


def get_transaction_list_by_user_id(user_id):
    transaction_list = Transaction.objects.filter(user_id=user_id)
    return transaction_list


def get_transaction_list_by_status(status):
    transaction_list = Transaction.objects.filter(status=status)
    return transaction_list


def get_transaction_by_id(transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    return transaction


def add_transaction(user_id, ttype, title, content):
    t = Transaction(user_id=user_id, ttype=ttype, title=title, content=content)
    t.save()


def update_transaction_by_id(transaction_id, attr):
    transaction = get_transaction_by_id(transaction_id)
    if 'status' in attr:
        if attr['status']:
            attr['status'] = transaction.status + 1
        else:
            attr['status'] = 0

    for key, value in attr.iteritems():
        transaction[key] = value

    transaction.save()




