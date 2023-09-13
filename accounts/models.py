from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, SlugField
from pages.models import Article


class CustomUser(AbstractUser):
    avatar = ImageField(upload_to='static/user-avatars', default='static/user-avatars/def_avatar.jpg')

    def __str__(self):
        return self.email
