from django.urls import path
from .views import (
    UserModelPostView,
    UserModelDetail,
    UserSearchView,
    UserPicturesPostView,
    UserPicturesDetailView,
    UserSetPasswordView,
    UserFollower,
    GetUserFollowers,
    GetUserFollows,
    EmailStatus,
    # Users
    # ThreadModelPostView,
    # ThreadModelDetailView,
    # MessageModelPostView,
)

urlpatterns = [
    path("UserModelPostView/", UserModelPostView.as_view(), name="UserModelPostView"),
    path(
        "UserModelDetail/", UserModelDetail.as_view(), name="UserModelDetail"
    ),
    path(
        "UserPicturesPostView/",
        UserPicturesPostView.as_view(),
        name="UserPicturesPostView",
    ),
    path(
        "UserPicturesDetailView/<int:pk>/",
        UserPicturesDetailView.as_view(),
        name="UserPicturesDetailView",
    ),
    path(
        "UserSetPasswordView/",
        UserSetPasswordView.as_view(),
        name="UserSetPasswordView",
    ),
    path("UserFollower/", UserFollower.as_view(), name="UserFollower"),
    path("GetUserFollowers/", GetUserFollowers.as_view(), name="GetUserFollowers"),
    path("GetUserFollows/", GetUserFollows.as_view(), name="GetUserFollows"),
    path("usersearch/", UserSearchView.as_view(), name="usersearch"),
    path("EmailStatus/", EmailStatus.as_view(), name="EmailStatus"),
    # path("Users/", Users.as_view(), name="Users"),
    # path(
    #     "ThreadModelPostView/<int:pk>/",
    #     ThreadModelPostView.as_view(),
    #     name="ThreadModelPostView",
    # ),
    # path(
    #     "ThreadModelDetailView/<int:pk>/",
    #     ThreadModelDetailView.as_view(),
    #     name="ThreadModelDetailView",
    # ),
    # path(
    #     "MessageModelPostView/<int:pk>/",
    #     MessageModelPostView.as_view(),
    #     name="MessageModelPostView",
    # ),
]
