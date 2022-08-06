from django.shortcuts import render

from django.views.generic import TemplateView
from .models import *


class IndexPage(TemplateView):
    def get(self, request, **kwargs):
        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:9]

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })

        promote_data = []

        all_promoted_articles = Article.objects.filter(promote=True)



        for promoted_article in all_promoted_articles:
            promote_data.append({
                'category': promoted_article.category,
                'cover': promoted_article.cover.url,
                'title': promoted_article.title,
                'author': promoted_article.author.user.username,
                'author_avatar': promoted_article.author.avatar.url if promoted_article.author.avatar else None,
                'created_at': promoted_article.created_at.date(),
            })

        context = {
            'article_data': article_data,
            'promote_date': promote_data,
        }

        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'