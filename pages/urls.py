from django.urls import path

from .views import HomePageView, AboutPageView, ExactArticlePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("articles/<int:pk>/", ExactArticlePageView.as_view(), name='article-page'),
]
