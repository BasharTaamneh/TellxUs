import os
from django.db import models
from django.urls import reverse


def upload_path(instance, filename):
    return "/".join(["files", str(instance.title), filename])


class Article(models.Model):
    owner = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    files = models.FileField(blank=True, null=True, upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Likes(models.Model):
    id = models.IntegerField(
        default=-1, blank=False, null=False, primary_key=True, unique=True
    )
    likes = models.IntegerField(default=0)
    deslikes = models.IntegerField(default=0)


class Comments(models.Model):
    id = models.IntegerField(
        default=-1, blank=False, null=False, primary_key=True, unique=True
    )
    comments = models.TextField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
