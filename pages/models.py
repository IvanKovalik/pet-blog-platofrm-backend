from django.db import models
from django.db.models import Model, CharField, DateTimeField, IntegerField, ImageField, ForeignKey, TextField
from django_project.settings import AUTH_USER_MODEL

from taggit.managers import TaggableManager


class Article(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    name = CharField(max_length=100, blank=False)
    text = TextField(max_length=5000)
    logo_image = ImageField(upload_to='static/article-images')
    
    likes = IntegerField(default=0)
    date_created = DateTimeField(auto_now=True)
    date_article_changed = DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name


class Comment(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    text = TextField(max_length=1000)
    date_created = DateTimeField(auto_now=True)
    date_article_changed = DateTimeField(auto_now_add=True)

    likes = IntegerField(default=0)

    def __str__(self):
        return self.text[:50]
