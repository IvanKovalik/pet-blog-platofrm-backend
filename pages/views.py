from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, CreateView
from .models import Article
from taggit.models import Tag
from .forms import ArticleCreateForm, CommentCreateForm

MAX_ARTICLES_ON_PAGE = 12


class HomePageView(View):
    template_name = "pages/home.html"

    def get(self, request):
        # from .services.fake_article_factory import create_many_articles
        # create_many_articles(100)

        context = {
            'articles': Article.objects.order_by('-date_article_created')[:MAX_ARTICLES_ON_PAGE],
            'tags': Tag.objects.all(),
            'top_viewed_articles': Article.objects.order_by('-views')[:5],
        }

        return render(request, self.template_name, context)

    def post(self, request):
        pass


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class ExactArticlePageView(CreateView):
    template_name = 'pages/exact-article-page.html'

    def get(self, request, *args, **kwargs):
        context = {
            'article': Article.objects.get(id=kwargs['id']),
            # 'comments':
        }
        article = Article.objects.get(id=kwargs['id'])
        article.views += 1
        article.save()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass


class ByTagArticleView(View):
    template_name = 'pages/by-tag-page.html'

    def get(self, request, tag_slug):
        tag_id = Tag.objects.get(slug__exact=tag_slug)
        context = {
            'articles': Article.objects.filter(tags=tag_id).order_by('-date_article_created')[:MAX_ARTICLES_ON_PAGE],
            'tags': Tag.objects.all(),
        }
        return render(request, self.template_name, context)


class CreateArticleView(CreateView):
    template_name = 'pages/create-article.html'

    def get(self, request, *args, **kwargs):
        form = ArticleCreateForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            form.instance.author_id = self.request.user.id
            form.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})


class CommentCreateView(CreateView):
    form_class = CommentCreateForm
    template_name = ''

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)

        return self.render_to_response({
            'form': form,
            'article': article
        })
