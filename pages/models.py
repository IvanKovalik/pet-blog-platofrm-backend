from django.db import models
from django.db.models import Model, CharField, DateTimeField, PositiveIntegerField, ImageField, ForeignKey, TextField, \
    OneToOneField, ManyToManyField
from django_project.settings import AUTH_USER_MODEL

from taggit.managers import TaggableManager


class Article(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    name = CharField(max_length=1000, blank=False)
    text = TextField(max_length=15000)
    logo_image = ImageField(upload_to='static/article-images', blank=True)

    views = PositiveIntegerField(default=0)
    date_changed = DateTimeField(auto_now=True)
    date_article_created = DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class Comment(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    text = TextField(max_length=1000)
    date_changed = DateTimeField(auto_now=True)
    date_article_created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]


class Like(Model):
    like_author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    # article = ManyToManyField(Article, models.DO_NOTHING)
    date_time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.like_author


class Article_views(Model):
    view_author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    # article = ManyToManyField(Article, models.DO_NOTHING)
    date_time = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.view_author
