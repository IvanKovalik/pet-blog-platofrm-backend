from django.contrib import admin
from .models import Article, Comment

# Register your models here.
# @admin.register(Article)
# class ModelNameAdmin(admin.ModelAdmin):
#     model = Article

admin.site.register(Article)
admin.site.register(Comment)
