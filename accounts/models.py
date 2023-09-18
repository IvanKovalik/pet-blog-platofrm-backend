from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, SlugField
from django.db import models
from pages.models import Article


class CustomUser(AbstractUser):
    avatar = ImageField(
        upload_to='static/user-avatars',
        default='static/user-avatars/def_avatar.jpg'
    )
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={'unique': "A user with that username already exists."},
    )
    email = models.EmailField(
        unique=True, blank=False,
        error_messages={'unique': "A user with that email already exists.", }
    )
    gender = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    about = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "gender"]

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.get_full_name()
