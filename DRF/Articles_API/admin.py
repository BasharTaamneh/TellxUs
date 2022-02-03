from django.contrib import admin
from .models import Article, ArticleFiles, ArticleComments, Notification


@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_filter = ("title", "owner")
    list_display = ("title", "id", "owner", "created_at")


@admin.register(ArticleFiles)
class ArticleFilesModel(admin.ModelAdmin):
    list_filter = ("article_id",)
    list_display = ("id", "article_id", "files")


@admin.register(ArticleComments)
class ArticleCommentsModel(admin.ModelAdmin):
    list_filter = ("owner", "article_id")
    list_display = ("id", "article_id", "owner", "comment")

admin.site.register(Notification)