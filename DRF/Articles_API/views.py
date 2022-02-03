from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse, response
from rest_framework.permissions import AllowAny
from django.db.models import Q
import shutil, os

from .models import (
    Article,
    ArticleFiles,
    ArticleComments,
    Notification,
)

from .serializers import (
    ArticleSerializer,
    ArticleFilesSerializer,
    ArticleCommentsSerializer,
    NotificationSerializer,
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

# //////////////////////////////////////////////////////////////////#
class ArticlePostView(ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            try:
                title = request.data["title"]
            except:
                return JsonResponse(
                    {
                        "title": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not title:
                return JsonResponse(
                    {
                        "title": "this feild could not be blank",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            try:
                description = request.data["description"]
            except:
                return JsonResponse(
                    {
                        "description": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                data = data = {
                    "title": title,
                    "description": description,
                    "owner": request.user.id,
                }
            except:
                return JsonResponse(
                    {
                        "title": "this feild is requierd",
                        "description": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                files = request.data["files"]
                files = request.FILES.getlist("files", None)
            except:
                return JsonResponse(
                    {
                        "files": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = ArticleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                if len(files):
                    article_id = Article.objects.latest("created_at")
                    for file in files:
                        article_files = ArticleFiles.objects.create(
                            files=file, article_id=article_id
                        )
                        article_files.save()
                return JsonResponse(
                    data=serializer.data, status=status.HTTP_201_CREATED
                )
            return JsonResponse(
                data=serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            if not len(self.get_queryset()):
                return JsonResponse(
                    {
                        "Articles": "There are no articles",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            articlehiles = Article.objects.all()
            serializer = ArticleSerializer(articlehiles, many=True)
            return JsonResponse(
                data=serializer.data,
                safe=False,
                status=status.HTTP_200_OK,
            )


# //////////////////////////////////////////////////////////////////#
class ArticleDetail(RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def update(self, request, *args, **kwargs):

        if request.method == "PUT":
            partial = kwargs.pop("pk")

            try:
                title = request.data["title"]
            except:
                return JsonResponse(
                    {
                        "title": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not title:
                return JsonResponse(
                    {
                        "title": "this feild could not be blank",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            try:
                description = request.data["description"]
            except:
                return JsonResponse(
                    {
                        "description": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                data = data = {
                    "title": title,
                    "description": description,
                }
            except:
                return JsonResponse(
                    {
                        "title": "this feild is requierd",
                        "description": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                files = request.data["files"]
                files = request.FILES.getlist("files", None)
            except:
                return JsonResponse(
                    {
                        "files": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                article = Article.objects.all().get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "Article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            old_files = ArticleFiles.objects.filter(article_id=partial)
            if len(old_files):
                fs = FileSystemStorage()
                for obj in old_files:
                    fs.delete(str(obj.files))
            old_files.delete()

            article = (
                Article.objects.all()
                .filter(id=partial)
                .update(title=title, description=description)
            )

            if len(files):
                article_id = Article.objects.all().get(id=partial)
                for file in files:
                    new_files = ArticleFiles.objects.create(
                        files=file, article_id=article_id
                    )
                    new_files.save()

            article = Article.objects.filter(id=partial)
            serializer = ArticleSerializer(article, many=True)
            if serializer:
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_202_ACCEPTED
                )
            return JsonResponse(
                serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            partial = kwargs.pop("pk")

            if os.path.isdir(
                f"media/user_id_{request.user.id}_files/articl_{partial}_user_{request.user.id}"
            ):
                shutil.rmtree(
                    f"media/user_id_{request.user.id}_files/articl_{partial}_user_{request.user.id}"
                )

            article = Article.objects.all().filter(id=partial)
            article.delete()
            return response.HttpResponse(status=status.HTTP_204_NO_CONTENT)


# //////////////////////////////////////////////////////////////////#
class ArticleFilesPostView(ListCreateAPIView):
    queryset = ArticleFiles.objects.all()
    serializer_class = ArticleFilesSerializer

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            return JsonResponse(
                {"detail": 'Method "POST" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            counte = ArticleFiles.objects.count()
            if not counte:
                return JsonResponse(
                    {
                        "Files": "There are no files",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            articlehiles = ArticleFiles.objects.all()
            serializer = ArticleFilesSerializer(articlehiles, many=True)
            return JsonResponse(
                data=serializer.data,
                safe=False,
                status=status.HTTP_200_OK,
            )


# //////////////////////////////////////////////////////////////////#
class ArticleSearchView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            try:
                keywords = request.data["keywords"]
            except KeyError:
                return JsonResponse(
                    {
                        "keywords": "KeyError search key ('keywords') is missing which should be in form-data"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not keywords:
                return JsonResponse(
                    {"keywords": f"inter a search keywords"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            articletitle = Article.objects.filter(Q(title__icontains=keywords))
            articledescription = Article.objects.filter(
                Q(description__icontains=keywords)
            )
            if not len(articletitle) and not len(articledescription):
                return JsonResponse(
                    {"keywords": f"No matching articles for {keywords}"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            serializer1 = ArticleSerializer(articletitle, many=True)
            serializer2 = ArticleSerializer(articledescription, many=True)
            if not len(serializer1.data):
                return JsonResponse(
                    {"discontain": serializer2.data},
                    safe=False,
                    status=status.HTTP_200_OK,
                )
            if not len(serializer2.data):
                return JsonResponse(
                    {"titcontain": serializer1.data},
                    safe=False,
                    status=status.HTTP_200_OK,
                )
            if len(serializer1.data) and len(serializer2.data):
                return JsonResponse(
                    {"discontain": serializer2.data, "titcontain": serializer1.data},
                    safe=False,
                    status=status.HTTP_200_OK,
                )
            return JsonResponse(
                {"discontain": serializer2.errors, "titcontain": serializer1.errors},
                safe=False,
                status=status.HTTP_400_BAD_REQUEST,
            )


# //////////////////////////////////////////////////////////////////#
class ArticlesLikes(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                article = Article.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            is_dislike = False
            for dislike in article.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break

            if is_dislike:
                article.dislikes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=2,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_anger = False
            for anger in article.anger_me.all():
                if anger == request.user:
                    is_anger = True
                    break
            if is_anger:
                article.anger_me.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=4,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_love = False
            for love in article.love_it.all():
                if love == request.user:
                    is_love = True
                    break
            if is_love:
                article.love_it.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=3,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_like = False
            for like in article.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if not is_like:
                article.likes.add(request.user)
                Notification.objects.create(
                    notification_type=1,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
            if is_like:
                article.likes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=1,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()
            return response.HttpResponse(status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class ArticlesDisLikes(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                article = Article.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            is_like = False
            for like in article.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if is_like:
                article.likes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=1,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_anger = False
            for anger in article.anger_me.all():
                if anger == request.user:
                    is_anger = True
                    break
            if is_anger:
                article.anger_me.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=4,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_love = False
            for love in article.love_it.all():
                if love == request.user:
                    is_love = True
                    break
            if is_love:
                article.love_it.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=3,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_dislike = False
            for dislike in article.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break
            if not is_dislike:
                article.dislikes.add(request.user)
                Notification.objects.create(
                    notification_type=2,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )

            if is_dislike:
                article.dislikes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=2,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()
            return response.HttpResponse(status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class ArticlesAnger(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                article = Article.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            is_like = False
            for like in article.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if is_like:
                article.likes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=1,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_dislike = False
            for dislike in article.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break
            if is_dislike:
                article.dislikes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=2,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_love = False
            for love in article.love_it.all():
                if love == request.user:
                    is_love = True
                    break
            if is_love:
                article.love_it.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=3,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_anger = False
            for anger in article.anger_me.all():
                if anger == request.user:
                    is_anger = True
                    break
            if not is_anger:
                article.anger_me.add(request.user)
                Notification.objects.create(
                    notification_type=4,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )

            if is_anger:
                article.anger_me.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=4,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()
            return response.HttpResponse(status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class ArticlesLove(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                article = Article.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            is_like = False
            for like in article.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if is_like:
                article.likes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=1,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )

                notification.delete()
            is_dislike = False
            for dislike in article.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break
            if is_dislike:
                article.dislikes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=2,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_anger = False
            for anger in article.anger_me.all():
                if anger == request.user:
                    is_anger = True
                    break
            if is_anger:
                article.anger_me.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=4,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()

            is_love = False
            for love in article.love_it.all():
                if love == request.user:
                    is_love = True
                    break
            if not is_love:
                article.love_it.add(request.user)
                Notification.objects.create(
                    notification_type=3,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )

            if is_love:
                article.love_it.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=3,
                    to_user=article.owner,
                    from_user=request.user,
                    article=article,
                )
                notification.delete()
            return response.HttpResponse(status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class ArticleCommentsPostView(ListCreateAPIView):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentsSerializer

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            counte = ArticleComments.objects.count()
            if not counte:
                return JsonResponse(
                    {
                        "Comments": "There are no comments",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            articlehiles = ArticleComments.objects.all()
            serializer = ArticleCommentsSerializer(articlehiles, many=True)
            return JsonResponse(
                data=serializer.data,
                safe=False,
                status=status.HTTP_200_OK,
            )

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                comment = request.data["comment"]
            except:
                return JsonResponse(
                    {
                        "comment": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not comment:
                return JsonResponse(
                    {
                        "comment": "this feild could not be blank",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            try:
                article = Article.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            comment = ArticleComments.objects.create(
                comment=comment, article_id=article, owner=request.user
            )
            Notification.objects.create(
                notification_type=7,
                to_user=article.owner,
                from_user=request.user,
                article=article,
                comment=comment,
            )
            serializer = ArticleCommentsSerializer(comment)
            if serializer:
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////#
class ArticleCommentsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentsSerializer

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            partial = kwargs.pop("pk")
            try:
                comment = request.data["comment"]
            except:
                return JsonResponse(
                    {
                        "comment": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not comment:
                return JsonResponse(
                    {
                        "comment": "this feild could not be blank",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            try:
                articlecomment = ArticleComments.objects.all().filter(pk=partial)
            except:
                return JsonResponse(
                    {
                        "comment": f"ArticleComments with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            articlecomment.update(comment=comment)
            articlecomment = ArticleComments.objects.get(pk=partial)
            serializer = ArticleCommentsSerializer(articlecomment)
            if serializer:
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////#
class CommentsReplyPostView(ListCreateAPIView):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentsSerializer

    def get(self, request, *args, **kwargs):

        if request.method == "GET":
            return JsonResponse(
                {
                    "detail": 'Method "GET" not allowed.',
                },
                status=status.HTTP_204_NO_CONTENT,
            )

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                comment = request.data["comment"]
            except:
                return JsonResponse(
                    {
                        "comment": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not comment:
                return JsonResponse(
                    {
                        "comment": "this feild could not be blank",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            try:
                parent_comment = request.data["parent_comment"]
            except:
                return JsonResponse(
                    {
                        "parent_comment": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not parent_comment:
                return JsonResponse(
                    {
                        "parent_comment": "this feild could not be blank",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            try:
                parent_comment = ArticleComments.objects.get(pk=parent_comment)
            except:
                return JsonResponse(
                    {
                        "articleComments": f"ArticleComments with ID: {parent_comment} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            try:
                article = Article.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "article": f"ArticleModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            comment = ArticleComments.objects.create(
                comment=comment,
                article_id=article,
                owner=request.user,
                parent=parent_comment,
            )
            Notification.objects.create(
                notification_type=8,
                to_user=article.owner,
                from_user=request.user,
                article=article,
                comment=comment,
            )
            serializer = ArticleCommentsSerializer(comment)
            if serializer:
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# //////////////////////////////////////////////////////////////////#
class CommentsLikes(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                comment = ArticleComments.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "comment": f"CommentModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            is_dislike = False
            for dislike in comment.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break
            if is_dislike:
                comment.dislikes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=10,
                    to_user=comment.owner,
                    from_user=request.user,
                    article=comment.article_id,
                    comment=comment,
                )
                notification.delete()

            is_like = False
            for like in comment.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if not is_like:
                comment.likes.add(request.user)
                Notification.objects.create(
                    notification_type=9,
                    to_user=comment.owner,
                    from_user=request.user,
                    article=comment.article_id,
                    comment=comment,
                )

            if is_like:
                comment.likes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=9,
                    to_user=comment.owner,
                    from_user=request.user,
                    article=comment.article_id,
                    comment=comment,
                )
                notification.delete()
            return response.HttpResponse(status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class CommentsDisLikes(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            partial = kwargs.pop("pk")
            try:
                comment = ArticleComments.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "comment": f"CommentModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            is_like = False
            for like in comment.likes.all():
                if like == request.user:
                    is_like = True
                    break
            if is_like:
                comment.likes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=9,
                    to_user=comment.owner,
                    from_user=request.user,
                    article=comment.article_id,
                    comment=comment,
                )
                notification.delete()

            is_dislike = False
            for dislike in comment.dislikes.all():
                if dislike == request.user:
                    is_dislike = True
                    break
            if not is_dislike:
                comment.dislikes.add(request.user)
                Notification.objects.create(
                    notification_type=10,
                    to_user=comment.owner,
                    from_user=request.user,
                    article=comment.article_id,
                    comment=comment,
                )
            if is_dislike:
                comment.dislikes.remove(request.user)
                notification = Notification.objects.all().filter(
                    notification_type=10,
                    to_user=comment.owner,
                    from_user=request.user,
                    article=comment.article_id,
                    comment=comment,
                )
                notification.delete()

            return response.HttpResponse(status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class NotificationGeter(ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            return JsonResponse(
                {"detail": 'Method "POST" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            counte = Notification.objects.count()
            if not counte:
                return JsonResponse(
                    {
                        "Notification": "There are no notifications",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            articlehiles = Notification.objects.all().filter(to_user=request.user.id)
            serializer = NotificationSerializer(articlehiles, many=True)
            if not len(serializer.data):
                return JsonResponse(
                    {
                        "Notification": "There are no notifications yet",
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
            return JsonResponse(
                data=serializer.data,
                safe=False,
                status=status.HTTP_200_OK,
            )


# //////////////////////////////////////////////////////////////////#
class NotificationHandler(RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            return JsonResponse(
                {"detail": 'Method "DELETE" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def update(self, request, *args, **kwargs):
        if request.method == "PATCH":
            return JsonResponse(
                {"detail": 'Method "PATCH" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        if request.method == "PUT":
            partial = kwargs.pop("pk")
            print(partial)
            try:
                notifications = Notification.objects.get(pk=partial)
            except:
                return JsonResponse(
                    {
                        "notifications": f"NotificationModel with ID: {partial} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            notifications = Notification.objects.all().filter(
                pk=partial, to_user=request.user.id, user_has_seen=False
            )
            notifications.update(user_has_seen=True)
            return JsonResponse(
                {"notifications": f"user_has_seen notification ID: {partial}."},
                status=status.HTTP_200_OK,
            )
