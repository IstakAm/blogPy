from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('contact/', views.ContactPage.as_view(), name='contact'),
    path('article/all', views.AllArticleAPIView.as_view(), name='all_articles'),
    path('article/', views.SingleArticleAPIView.as_view(), name='single_article'),
    path('article/search/', views.SearchArticleAPIView.as_view(), name='search_article'),
    path('article/submit/', views.SubmitArticleAPIView.as_view(), name='submit_article'),
    path('article/update-cover/', views.UpdateArticleAPIView.as_view(), name='update_article'),
    path('article/delete/', views.DeleteArticleAPIView.as_view(), name='delete_article'),

]
