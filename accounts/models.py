from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, SlugField


class CustomUser(AbstractUser):
    avatar = ImageField(upload_to='static/user-avatars', default='static/user-avatars/def_avatar.jpg')
    # slug = SlugField()

    def __str__(self):
        return self.email
