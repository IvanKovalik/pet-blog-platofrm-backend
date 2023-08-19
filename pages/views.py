from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, CreateView
from .models import Article
from taggit.models import Tag
from .forms import ArticleCreateForm
from accounts.models import CustomUser

MAX_ARTICLES_ON_PAGE = 12


class HomePageView(View):
    template_name = "pages/home.html"

    @staticmethod
    def get_best_authors():
        # TODO I think there is some django methods or technique to do this

        max_id = CustomUser.objects.order_by('-id').values('id').first()['id']
        best_authors = {}
        views_per_user = []
        for i in range(1, max_id + 1, 1):
            article_views_per_user = Article.objects.filter(author_id=i).values('views')
            for j in article_views_per_user:
                views_per_user.append(j['views'])

            best_authors[i] = sum(views_per_user)
            views_per_user.clear()

        best_authors = sorted(best_authors.items())
        print(best_authors)

        return best_authors

    def get(self, request):
        context = {
            'articles': Article.objects.order_by('-date_article_created')[:MAX_ARTICLES_ON_PAGE],
            'tags': Tag.objects.all(),
            'top_viewed_articles': Article.objects.order_by('-views')[:5],
            # 'top-viewed-authors': Article.objects.order_by('')
        }

        # self.get_best_authors()

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
