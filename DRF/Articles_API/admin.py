from django.contrib import admin
from .models import Article, Likes, Comments

@admin.register(Article)
class ArticleModel(admin.ModelAdmin):
    list_filter = ("title", "owner")
    list_display = ( "title", "id", "owner")

@admin.register(Likes)
class LikesModel(admin.ModelAdmin):
    list_filter = ("likes", "deslikes")
    list_display = ("id",)