
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def upload_path(instance, filename):
    user_id = instance.user_id.pk
    return "/".join(["profiles", f"user_id_{user_id}_profilepic", filename])


class UserModel(AbstractUser):

    GENDERS = (("Male", "Male"), ("Female", "Female"), ("Other", "Other"))

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(null=True, max_length=255, choices=GENDERS)
    city = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    follows = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="user_follows"
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="user_followers"
    )
    

    def __str__(self):
        return self.username

    def __int__(self):
        return self.pk


class UserPicturesModel(models.Model):
    user_id = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, null=True, blank=False
    )
    profile_photo = models.ImageField(
        default="static/blank_profile_image.png",
        blank=True,
        null=True,
        upload_to=upload_path,
    )

    def delete(self, *args, **kwargs):
        fs = FileSystemStorage()
        fs.delete(str(self.profile_photo))
        self.profile_photo.delete()
        super().delete(*args, **kwargs)


# class ThreadModel(models.Model):
#     sender = models.ForeignKey("UserModel", on_delete=models.CASCADE, related_name='+')
#     receiver = models.ForeignKey("UserModel", on_delete=models.CASCADE, related_name='+')
#     class Meta:
#         ordering = ["-id"]


# class MessageModel(models.Model):
# 	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
# 	sender_user = models.ForeignKey("UserModel", on_delete=models.CASCADE, related_name='+')
# 	receiver_user = models.ForeignKey("UserModel", on_delete=models.CASCADE, related_name='+')
# 	massage = models.TextField(blank=True, null=True)
# 	date = models.DateTimeField(default=timezone.now)
# 	is_read = models.BooleanField(default=False)