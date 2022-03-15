from rest_framework import serializers
from .models import UserModel, UserPicturesModel#, ThreadModel, MessageModel
from rest_framework_simplejwt.tokens import RefreshToken


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "gender",
            "birth_date",
            "follows",
            "followers",
            "city",
            "email",
            "bio",
            "password",
            "last_login",
            "date_joined",
        )

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        RefreshToken.for_user(user)
        return user


class UserPicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPicturesModel
        fields = "__all__"


# class ThreadModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ThreadModel
#         fields = "__all__"


# class MessageModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MessageModel
#         fields = "__all__"
