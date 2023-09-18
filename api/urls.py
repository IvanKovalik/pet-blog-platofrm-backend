from api.views import ListArticles, DetailArticle, ListComments, DetailComment, ListUsers

from django.urls import path

urlpatterns = [
    path('articles/', ListArticles.as_view()),
    path('articles/<str:pk>', DetailArticle.as_view()),
    
    path('comments/', ListComments.as_view()),
    path('comments/<str:pk>', DetailComment.as_view()),
    
    path('all-users/', ListUsers.as_view()),
]