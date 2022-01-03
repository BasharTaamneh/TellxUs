from django.urls import path
from .views import (
    ArticleGetView,
    ArticleSearchView,
    ArticlePostView,
    ArticleUpdateView,
    ArticleDeleteView,
    LikesView
)

urlpatterns = [
    path(
        "AddArticlse/", ArticlePostView.as_view(), name="AddArticlse"
    ),  # add new article (POST) return it's json data
    path(
        "json_Articles/", ArticleGetView.as_view(), name="json_Articles"
    ),  # view all articles in json format (GET)
    path(
        "ArticlesSearch/", ArticleSearchView.as_view(), name="ArticlesSearch"
    ),  # search for articles py title (GET)
    path(
        "ArticlesUpdate/", ArticleUpdateView.as_view(), name="ArticlesUpdate"
    ),  # update article (PUT)
    path(
        "ArticlesDelete/", ArticleDeleteView.as_view(), name="ArticlesDelete"
    ),  # delete article (DELETE)
    path("ArticlesLikes/", LikesView.as_view(), name="ArticlesLikes"),
    # create & update & get articles likes (POST, GET, PUt)
]
