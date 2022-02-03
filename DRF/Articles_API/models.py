from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.utils import timezone


def upload_path(instance, filename):
    return "/".join(
        [
            f"user_id_{instance.article_id.owner.pk}_files",
            f"articl_{instance.article_id.pk}_user_{instance.article_id.owner.pk}",
            filename,
        ]
    )


class Article(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=False
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name="likes")
    dislikes = models.ManyToManyField(
        get_user_model(), blank=True, related_name="dislikes"
    )
    anger_me = models.ManyToManyField(
        get_user_model(), blank=True, related_name="anger_me"
    )
    love_it = models.ManyToManyField(
        get_user_model(), blank=True, related_name="love_it"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def __int__(self):
        return self.pk


class ArticleFiles(models.Model):
    article_id = models.ForeignKey(
        Article, on_delete=models.CASCADE, null=True, blank=False
    )
    files = models.FileField(blank=True, null=True, upload_to=upload_path)

    def __int__(self):
        return self.pk

    def delete(self, *args, **kwargs):
        fs = FileSystemStorage()
        fs.delete(str(self.files))
        self.files.delete()
        super().delete(*args, **kwargs)


class ArticleComments(models.Model):
    comment = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        get_user_model(), blank=True, related_name="comment_likes"
    )
    dislikes = models.ManyToManyField(
        get_user_model(), blank=True, related_name="comment_dislikes"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="+"
    )

    @property
    def children(self):
        return ArticleComments.objects.filter(parent=self).order_by("-created_on").all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


class Notification(models.Model):
    # **Notification Types**
    #  1 --> like_articl.
    #  2 --> dislike_articl.
    #  3 --> love_it_articl.
    #  4 --> anger_me_articl.
    #  5 --> follow.
    #  6 --> unfollow.
    #  7 --> comment.
    #  8 --> replycomment.
    #  9 --> like_comment.
    #  10 --> dislike_comment.

    notification_type = models.IntegerField()
    to_user = models.ForeignKey(
        get_user_model(),
        related_name="notification_to",
        on_delete=models.CASCADE,
        null=True,
    )
    from_user = models.ForeignKey(
        get_user_model(),
        related_name="notification_from",
        on_delete=models.CASCADE,
        null=True,
    )
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="+", blank=True, null=True
    )
    comment = models.ForeignKey(
        "ArticleComments",
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]
