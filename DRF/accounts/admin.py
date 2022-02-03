from django.contrib import admin
from .models import UserModel, UserPicturesModel


@admin.register(UserModel)
class UserAdminModel(admin.ModelAdmin):
    list_filter = ("id", "gender", "birth_date", "city", "last_login", "date_joined")
    list_display = (
        "username",
        "email",
        "id",
        "city",
        "birth_date",
        "gender",
        "last_login",
        "date_joined",
    )


@admin.register(UserPicturesModel)
class UserPicturesAdminModel(admin.ModelAdmin):
    list_filter = ("id", "user_id")
    list_display = ("profile_photo", "id", "user_id")
