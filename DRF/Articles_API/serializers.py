from rest_framework import serializers

from .models import Article, Likes, Comments


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "files",
            "created_at",
            "updated_at",
        ]


class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "description", "files", "created_at", "updated_at"]


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ["id", "likes", "deslikes"]


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["id", "comments", "created_at"]
