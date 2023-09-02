from accounts.models import CustomUser
import string
import random


def __create_password():
    length = random.randint(10, 15)
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return password


def __create_email():
    length = random.randint(7, 11)
    email = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    email += random.choice(['@mail.com', '@mail.ru', '@gmail.com', '@yandex.ru', '@yahoo.com'])
    return email


def __create_username():
    length = random.randint(7, 11)
    username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return username


def create_many_users(number_of_users: int):
    for i in range(number_of_users):
        CustomUser.objects.create_user(
            email=__create_email(),
            username=__create_username(),
            password=__create_password(),
        )
