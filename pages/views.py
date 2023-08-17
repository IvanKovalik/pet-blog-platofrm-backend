from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Article
from accounts.models import CustomUser
from taggit.models import Tag


class HomePageView(View):
    template_name = "pages/home.html"

    def get(self, request):
        context = {
            'articles': Article.objects.all(),
            'tags': Tag.objects.all(),

        }
        return render(request, self.template_name, context)


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class ExactArticlePageView(View):
    template_name = 'pages/exact-article-page.html'

    def get(self, request, pk):
        context = {
            'exact_article': Article.objects.filter(pk=pk)
        }
        return render(request, self.template_name, context)
