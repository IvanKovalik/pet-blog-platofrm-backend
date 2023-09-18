from collections.abc import Iterable
from django.db import models
from django.db.models import Model, CharField, DateTimeField, PositiveIntegerField, ImageField, ForeignKey, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_project.settings import AUTH_USER_MODEL

from taggit.managers import TaggableManager


class Article(Model):
    author = ForeignKey(
        AUTH_USER_MODEL,
        models.DO_NOTHING,
        help_text='This is authors ID'
    )
    name = CharField(max_length=1000, blank=False)
    text = TextField(max_length=25000)
    logo_image = ImageField(upload_to='static/article-images', blank=True)

    reading_time = PositiveIntegerField(default=None, null=True, blank=False)
    views = PositiveIntegerField(default=0)
    likes = PositiveIntegerField(default=0)
    date_changed = DateTimeField(auto_now=True)
    date_article_created = DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    def __str__(self):
        return self.name

    def body_to_string(self):
        return self.text

    class Meta:
        ordering = ['-article_order', '-pub_time']
        verbose_name = _('article')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def get_absolute_url(self):
        return reverse('article-page', kwargs={'article_id': self.id})

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])
        
    def liked(self):
        self.liked += 1
        self.save(update_fields=['likes'])

    def next_article(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()

    def prev_article(self):
        return Article.objects.filter(id__lt=self.id).first()


class Comment(Model):
    author = ForeignKey(AUTH_USER_MODEL, models.DO_NOTHING)
    article = ForeignKey(Article, models.CASCADE)
    text = TextField(max_length=1000)
    date_changed = DateTimeField(auto_now=True)
    date_comment_created = DateTimeField(auto_now_add=True)
    is_enable = models.BooleanField(_('enable'), default=False, blank=False, null=False)
    slug = models.SlugField(_("This is slug"))

    class Meta:
        ordering = ['-id']
        verbose_name = _('comment')
        verbose_name_plural = verbose_name
        get_latest_by = 'date_article_created'
        
    

    def __str__(self):
        return self.text
