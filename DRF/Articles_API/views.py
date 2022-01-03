from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Article, Comments, Likes
from .serializers import ArticleSerializer, ArticleUpdateSerializer, CommentsSerializer, LikesSerializer
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse

import time

# from django.views.decorators.csrf import csrf_exempt

# from rest_framework import status


class ArticlePostView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticated,)

    def post(
        self, request, *args, **kwargs
    ):  # add new article (POST) return it's json data

        if request.method == "POST":

            try:
                title_exists = request.data["title"]
                description_exists = request.data["description"]
                owner_exists = request.data["owner"]
            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError one or more (' title ', ' description ', ' owner ') is missing which should be in the body of the request"
                    },
                    status=400,
                )

            if (
                title_exists == "undefined"
                or title_exists == ""
                or description_exists == "undefined"
                or description_exists == ""
                or owner_exists == "undefined"
                or owner_exists == ""
            ):
                return JsonResponse(
                    {
                        "detail": "one of the fields is undefined (title, description, owner)"
                    },
                    status=204,
                )

            title = request.data["title"]
            description = request.data["description"]
            owner = request.data["owner"]

            if request.data["files"] != "undefined":

                files = request.data["files"]
                
                Article.objects.create(
                    title=title, description=description, owner=owner, files=files
                )

            else:
                Article.objects.create(
                    title=title, description=description, owner=owner, files=None
                )

            articles = Article.objects.filter(owner=owner)
            serializer = ArticleSerializer(articles, many=True)

            if serializer:
                return JsonResponse(serializer.data[-1], safe=False, status=201)
            return JsonResponse(serializer.errors, safe=False, status=400)


class ArticleGetView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):  # view all articles in json format (GET)

        if request.method == "GET":
            articles = Article.objects.all()
            counte = Article.objects.count()
            serializer = ArticleSerializer(articles, many=True)

            if not counte:
                return JsonResponse({"detail": "There is no Articles"}, status=204)
            return JsonResponse(
                serializer.data,
                safe=False,
                status=200,
            )


class ArticleSearchView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = (IsAuthenticated,)

    def get(
        self, request, *args, **kwargs
    ):  # search py title (GET) key should be in the body of the request

        if request.method == "GET":
            try:
                title = request.data["title"]
            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError search key (' title') is missing which should be in the body of the request"
                    },
                    status=400,
                )

            try:
                articles = Article.objects.get(title=title)
            except Article.DoesNotExist:
                return JsonResponse(
                    {"detail": "There are no match Articles"}, status=204
                )

            articles = Article.objects.all().filter(title=title)
            serializer = ArticleSerializer(articles, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)


class ArticleUpdateView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer
    # permission_classes = (IsAuthenticated,)

    def put(
        self, request, *args, **kwargs
    ):  # update article (PUT) return it's json data

        if request.method == "PUT":
            try:
                id = request.data["id"]
            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError (' id ') is missing which should be in the body of the request"
                    },
                    status=400,
                )
            if id != "" and id != "undefined":
                try:
                    article = Article.objects.get(id=id)
                except Article.DoesNotExist:
                    return JsonResponse(
                        {"detail": " id value is not found "}, status=204
                    )
            else:
                return JsonResponse({"detail": " Article not found "}, status=204)

            try:
                title_exists = request.data["title"]
                description_exists = request.data["description"]

            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError one ore more (' title ', ' description ') is missing which should be in the body of the request"
                    },
                    status=400,
                )

            if (
                title_exists == ""
                or title_exists == "undefined"
                or description_exists == ""
                or description_exists == "undefined"
            ):
                return JsonResponse(
                    {
                        "detail": "one or more of the fields is undefined (title, description)"
                    },
                    status=204,
                )

            title = request.data["title"]
            description = request.data["description"]

            try:
                request.data["files"]
            except:
                return JsonResponse(
                    {
                        "detail": "KeyError  ('files') is missing which should be in the body of the request"
                    },
                    status=400,
                )

            if request.data["files"] != "undefined" or request.data["files"] != "":

                files = request.data["files"]

                time_updated = time.strftime("%Y-%m-%d")
                sf = FileSystemStorage()
                file_name = files.name
                file = sf.save(f"files/{title}_{time_updated}/{file_name}", files)
                fileurl = sf.url(file)

                article = Article.objects.filter(id=id).update(
                    title=title,
                    description=description,
                    files=fileurl[7:].replace("%20", " "),
                )

            else:
                article = Article.objects.filter(id=id).update(
                    title=title, description=description, files=None
                )

            article = Article.objects.filter(id=id)
            serializer = ArticleSerializer(article, many=True)

            if serializer:
                return JsonResponse(serializer.data, safe=False, status=202)
            return JsonResponse(serializer.errors, safe=False, status=400)


class ArticleDeleteView(APIView):
    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer
    # permission_classes = (IsAuthenticated,)

    def delete(
        self, request, *args, **kwargs
    ):  # update article (PUT) return it's json data

        if request.method == "DELETE":
            try:
                id = request.data["id"]
            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError (' id ') is missing which should be in the body of the request"
                    },
                    status=400,
                )
            if id != "" and id != "undefined":
                try:
                    Article.objects.get(id=id)
                except Article.DoesNotExist:
                    return JsonResponse(
                        {"detail": " id value is not found "}, status=204
                    )
            else:
                return JsonResponse({"detail": " Article not found "}, status=204)

            Article.objects.filter(id=id).delete()
            return JsonResponse({"detail": f" Article deleted id: {id} "}, status=200)


class LikesView(APIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    # permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        if request.method == 'PUT':
            try:
                id = request.data["id"]
            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError (' id ') is missing which should be in the body of the request"
                    },
                    status=400,
                )
            if id != "" and id != "undefined":
                try:
                    likes = Article.objects.get(id=id)
                except Article.DoesNotExist:
                    return JsonResponse(
                        {"detail": " id value is not found "}, status=204
                    )
            else:
                return JsonResponse({"detail": " Likes not found "}, status=204)

            try:
                likes_exists = request.data["likes"]
                deslikes_exists = request.data["deslikes"]

            except KeyError:
                return JsonResponse(
                    {
                        "detail": "KeyError one ore more (' deslikes ', ' likes ') is missing which should be in the body of the request"
                    },
                    status=400,
                )

            if (
                likes_exists == ""
                or likes_exists == "undefined"
                or deslikes_exists == ""
                or deslikes_exists == "undefined"
            ):
                return JsonResponse(
                    {
                        "detail": "one or more of the fields is undefined (deslikes, likes)"
                    },
                    status=204,
                )

            deslikes = request.data["deslikes"]
            likes = request.data["likes"]

            likes = Likes.objects.filter(id=id).update(
                    deslikes=deslikes, likes=likes
                )

            likes = Likes.objects.filter(id=id)
            serializer = LikesSerializer(likes, many=True)

            if serializer:
                return JsonResponse(serializer.data, safe=False, status=202)
            return JsonResponse(serializer.errors, safe=False, status=400)
    
    
    def get(self, request, *args, **kwargs):  # view all articles (likes, deslikes) in json format (GET)

        if request.method == "GET":
            likes = Likes.objects.all()
            counte = Likes.objects.count()
            serializer = LikesSerializer(likes, many=True)

            if not counte:
                return JsonResponse({"detail": "There is no Articles (likes, deslikes)"}, status=204)
            return JsonResponse(
                serializer.data,
                safe=False,
                status=200,
            )

    