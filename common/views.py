from rest_framework.generics import ListAPIView
from common.models import Article
from common.serializers import ArticleSerializer


class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.all().order_by('-id')[:4]
    serializer_class = ArticleSerializer
