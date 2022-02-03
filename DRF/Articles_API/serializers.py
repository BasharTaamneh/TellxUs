from rest_framework import serializers
from .models import Article, ArticleFiles, ArticleComments, Notification


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleFiles
        fields = "__all__"


class ArticleCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComments
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
