from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, SlugField
from pages.models import Article


class CustomUser(AbstractUser):
    avatar = ImageField(upload_to='static/user-avatars', default='static/user-avatars/def_avatar.jpg')

    # slug = SlugField()

    @staticmethod
    def count_views(self):
        views = 0
        articles = Article.objects.filter(author_id=self.id)
        for article in articles:
            views += article.objects.values('views')
            pass

    def __str__(self):
        return self.email
