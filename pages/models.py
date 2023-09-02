from django.db import models
from django.db.models import Model, CharField, DateTimeField, PositiveIntegerField, ImageField, ForeignKey, TextField, \
    OneToOneField, ManyToManyField
from django_project.settings import AUTH_USER_MODEL

from taggit.managers import TaggableManager


class Article(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    name = CharField(max_length=1000, blank=False)
    text = TextField(max_length=25000)
    logo_image = ImageField(upload_to='static/article-images', blank=True)

    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    date_changed = DateTimeField(auto_now=True)
    date_article_created = DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    @staticmethod
    def get_reading_time_in_seconds(self):
        spaces = self.text.count(' ')
        return spaces // 120

    def __str__(self):
        return self.name


class Comment(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    text = TextField(max_length=1000)
    date_changed = DateTimeField(auto_now=True)
    date_article_created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
