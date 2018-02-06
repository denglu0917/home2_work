from firstapp.models import Article
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        # fields = ('title', 'content',)


@api_view(['GET'])
def article(request):
    article_list = Article.objects.all()
    serializer = ArticleSerializer(article_list, many=True)
    return Response(serializer.data)
