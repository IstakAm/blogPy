from django.shortcuts import render

from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers




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


class AllArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:10]
            data = []
            for article in all_articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.first_name + " " + article.author.user.last_name,
                    'promote': article.promote,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialized_data = serializers.SingleArticleSerializer(article, many=True)
            data = serialized_data.data
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            from django.db.models import Q

            query = request.GET['query']

            data = []

            articles = Article.objects.filter(Q(content__icontains=query))
            for article in articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.first_name + " " + article.author.user.last_name,
                    'promote': article.promote,
                })

            return Response({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubmitArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status': "Bad request"}, status=status.HTTP_400_BAD_REQUEST)

            author = UserProfile.objects.get(id=author_id)
            category = Category.objects.get(id=category_id)
            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            article = Article.objects.get(id = article_id)
            article.cover = cover
            article.save()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)


        except:
            return Response({'status': "Internal server error , We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({'status': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
            Article.objects.get(id=article_id).delete()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

