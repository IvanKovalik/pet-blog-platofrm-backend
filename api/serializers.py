from accounts.models import CustomUser
from pages.models import Article, Comment

from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = ['author', 'name', 'text', 'views', 'likes', 'date_article_created', 'tags']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'gender', 'status', 'about']
        
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ['author', 'article', 'date_comment_created', 'is_enable']