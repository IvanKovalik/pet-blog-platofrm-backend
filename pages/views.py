from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Article
from taggit.models import Tag


class HomePageView(View):
    template_name = "pages/home.html"

    def get(self, request):
        context = {
            'articles': Article.objects.all(),
            'tags': Tag.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class ExactArticlePageView(View):
    template_name = 'pages/exact-article-page.html'

    def get(self, request, id):
        context = {
            'article': Article.objects.get(id=id),
        }
        article = Article.objects.get(id=id)
        article.views += 1
        article.save()
        
        return render(request, self.template_name, context)


class ByTagArticleView(View):
    template_name = 'pages/by-tag-page.html'

    def get(self, request, tag_slug):
        tag_id = Tag.objects.get(slug__exact=tag_slug)
        context = {
            'articles': Article.objects.filter(tags=tag_id),
            'tags': Tag.objects.all(),
        }
        return render(request, self.template_name, context)
