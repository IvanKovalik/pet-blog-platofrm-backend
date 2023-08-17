from django.urls import path

from .views import HomePageView, AboutPageView, ExactArticlePageView, ByTagArticleView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("articles/<int:id>/", ExactArticlePageView.as_view(), name='article-page'),
    path("articles/by-tag/<slug:tag_slug>/", ByTagArticleView.as_view(), name='articles-by-tag-page'),

]
