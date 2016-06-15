from auth.models import User
from common.utils import md5


def add_user(card_id, username, password, age, sex, department, position, mobile, emergency_contact, email):
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
        email=email
    )

    user.save()


def get_user(username):
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    return user
