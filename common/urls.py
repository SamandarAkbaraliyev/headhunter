from django.urls import path
from common.views import ArticleListAPIView

urlpatterns = [
    path('articles/', ArticleListAPIView.as_view()),
]
