from django.urls import path
from .views import (
    ArticlePostView,
    ArticleDetail,
    ArticleFilesPostView,
    ArticleSearchView,
    ArticlesLikes,
    ArticlesDisLikes,
    ArticlesAnger,
    ArticlesLove,
    ArticleCommentsPostView,
    ArticleCommentsDetailView,
    CommentsReplyPostView,
    CommentsLikes,
    CommentsDisLikes,
    NotificationGeter,
    NotificationHandler,
)

urlpatterns = [
    path("ArticlePostView/", ArticlePostView.as_view(), name="ArticlePostView"),
    path("ArticleDetail/<int:pk>/", ArticleDetail.as_view(), name="ArticleDetail"),
    path(
        "ArticleFilesPostView/",
        ArticleFilesPostView.as_view(),
        name="ArticleFilesPostView",
    ),
    path("ArticleSearchView/", ArticleSearchView.as_view(), name="ArticleSearchView"),
    path("ArticlesLikes/<int:pk>/", ArticlesLikes.as_view(), name="ArticlesLikes"),
    path(
        "ArticlesDisLikes/<int:pk>/",
        ArticlesDisLikes.as_view(),
        name="ArticlesDisLikes",
    ),
    path("ArticlesLove/<int:pk>/", ArticlesLove.as_view(), name="ArticlesLove"),
    path("ArticlesAnger/<int:pk>/", ArticlesAnger.as_view(), name="ArticlesAnger"),
    path(
        "ArticleCommentsPostView/<int:pk>/",
        ArticleCommentsPostView.as_view(),
        name="ArticleCommentsPostView",
    ),
    path(
        "ArticleCommentsDetailView/<int:pk>/",
        ArticleCommentsDetailView.as_view(),
        name="ArticleCommentsDetailView",
    ),
    path(
        "CommentsReplyPostView/<int:pk>/",
        CommentsReplyPostView.as_view(),
        name="CommentsReplyPostView",
    ),
    path("CommentsLikes/<int:pk>/", CommentsLikes.as_view(), name="CommentsLikes"),
    path(
        "CommentsDisLikes/<int:pk>/",
        CommentsDisLikes.as_view(),
        name="CommentsDisLikes",
    ),
    path(
        "NotificationGeter/",
        NotificationGeter.as_view(),
        name="NotificationGeter",
    ),
    path(
        "NotificationHandler/<int:pk>/",
        NotificationHandler.as_view(),
        name="NotificationHandler",
    ),
]
