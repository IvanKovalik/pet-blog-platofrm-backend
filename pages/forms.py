import logging
from django import forms

from .models import Article, Comment

logger = logging.getLogger(__name__)


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'name',
            'text',
            'logo_image',
            'tags'
        ]


class CommentCreateForm(forms.ModelForm):
    parent_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = [
            'text',
        ]


class BlogSearchForm(forms.Form):
    query = forms.CharField(required=True)

    def search(self):
        datas = super(BlogSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['query']:
            logger.info(self.cleaned_data['query'])
        return datas
