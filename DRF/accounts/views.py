import shutil, os, smtplib, random, re
from django.http import JsonResponse, response
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from Articles_API.models import Notification

from .models import UserModel, UserPicturesModel#, MessageModel, ThreadModel

from .serializers import (
    UserModelSerializer,
    UserPicturesSerializer,
    # ThreadModelSerializer,
    # MessageModelSerializer,
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

# //////////////////////////////////////////////////////////////////#
class UserModelPostView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):

        if request.method == "POST":
            try:
                username = request.data["username"]
            except:
                return JsonResponse(
                    {
                        "username": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not username:
                return JsonResponse(
                    {
                        "username": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            try:
                email = request.data["email"]
            except:
                return JsonResponse(
                    {
                        "email": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not email:
                return JsonResponse(
                    {
                        "email": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            try:
                password = request.data["password"]
            except:
                return JsonResponse(
                    {
                        "password": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not password:
                return JsonResponse(
                    {
                        "password": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            try:
                gender = request.data["gender"]
            except:
                return JsonResponse(
                    {
                        "gender": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                city = request.data["city"]
            except:
                return JsonResponse(
                    {
                        "city": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                birth_date = request.data["birth_date"]
            except:
                return JsonResponse(
                    {
                        "birth_date": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                about_me = request.data["about_me"]
            except:
                return JsonResponse(
                    {
                        "about_me": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                profile_photo = request.data["profile_photo"]
            except:
                return JsonResponse(
                    {
                        "profile_photo": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not len(profile_photo):
                profile_photo = "/static/blank_profile_image.png"

            data = {
                "username": username,
                "email": email,
                "password": password,
                "gender": gender,
                "city": city,
                "birth_date": birth_date,
                "about_me": about_me,
            }

            serializer = UserModelSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                user_id = UserModel.objects.latest("date_joined")
                user_picture = UserPicturesModel.objects.create(
                    profile_photo=profile_photo, user_id=user_id
                )
                user_picture.save()
                return JsonResponse(
                    data=serializer.data, status=status.HTTP_201_CREATED
                )
            return JsonResponse(
                data=serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
            )


# //////////////////////////////////////////////////////////////////#
class UserModelDetail(RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer

    def update(self, request, *args, **kwargs):

        if request.method == "PUT":

            partial = kwargs.pop("pk")

            try:
                current_password = request.data["current_password"]
            except:
                return JsonResponse(
                    {
                        "current_password": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not current_password:
                return JsonResponse(
                    {
                        "current_password": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            old_password = UserModel.objects.all().get(id=partial).password
            password_isvalid = check_password(current_password, old_password)

            if password_isvalid:

                user = UserModel.objects.all().filter(id=partial)

                try:
                    username = request.data["username"]
                except:
                    return JsonResponse(
                        {
                            "username": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if username:
                    try:
                        user.update(username=username)
                    except:
                        return JsonResponse(
                            {
                                "username": "user with this username already exists.",
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

                try:
                    email = request.data["email"]
                except:
                    return JsonResponse(
                        {
                            "email": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if email:

                    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
                    if not (re.fullmatch(regex, email)):
                        return JsonResponse(
                            {
                                "email": "please enter a valid email address.",
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

                    try:
                        user.update(email=email)
                    except:
                        return JsonResponse(
                            {
                                "email": "user with this email already exists.",
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

                try:
                    password = request.data["password"]
                except:
                    return JsonResponse(
                        {
                            "password": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if password:
                    new_password = make_password(password)
                    user.update(password=new_password)

                try:
                    gender = request.data["gender"]
                except:
                    return JsonResponse(
                        {
                            "gender": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if gender:
                    user.update(gender=gender)

                try:
                    city = request.data["city"]
                except:
                    return JsonResponse(
                        {
                            "city": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if city:
                    user.update(city=city)

                try:
                    birth_date = request.data["birth_date"]
                except:
                    return JsonResponse(
                        {
                            "birth_date": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if birth_date:
                    user.update(birth_date=birth_date)

                try:
                    about_me = request.data["about_me"]
                except:
                    return JsonResponse(
                        {
                            "about_me": "this feild is requierd",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if about_me:
                    user.update(about_me=about_me)

                serializer = UserModelSerializer(user, many=True)
                if serializer:
                    return JsonResponse(
                        serializer.data, safe=False, status=status.HTTP_202_ACCEPTED
                    )
                return JsonResponse(
                    serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
                )

            return JsonResponse(
                {
                    "current_password": "current password is not correct.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            partial = kwargs.pop("pk")
            try:
                current_password = request.data["current_password"]
            except:
                return JsonResponse(
                    {
                        "current_password": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not current_password:
                return JsonResponse(
                    {
                        "current_password": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            try:
                UserModel.objects.all().get(id=partial)
            except:
                return JsonResponse(
                    {
                        "detail": "Not found.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            old_password = UserModel.objects.all().get(id=partial).password
            password_isvalid = check_password(current_password, old_password)

            if password_isvalid:
                user = UserModel.objects.filter(id=partial)
                if len(user):
                    if os.path.isdir(f"media/profiles/user_id_{partial}_profilepic"):
                        shutil.rmtree(f"media/profiles/user_id_{partial}_profilepic")
                    if os.path.isdir(f"media/user_id_{partial}_files"):
                        shutil.rmtree(f"media/user_id_{partial}_files")
                    user.delete()
                    return response.HttpResponse(status=status.HTTP_204_NO_CONTENT)
                return JsonResponse(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            return JsonResponse(
                {
                    "current_password": "current password is not correct.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


# //////////////////////////////////////////////////////////////////#
class UserPicturesPostView(ListCreateAPIView):
    queryset = UserPicturesModel.objects.all()
    serializer_class = UserPicturesSerializer

    def create(self, request, *args, **kwargs):

        if request.method == "POST":
            try:
                profile_photo = request.data["profile_photo"]
            except:
                return JsonResponse(
                    {
                        "profile_photo": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not profile_photo:
                return JsonResponse(
                    {
                        "profile_photo": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            user_id = request.user
            photo = UserPicturesModel.objects.create(
                user_id=user_id, profile_photo=profile_photo
            )
            photo.save()
            serializer = UserPicturesSerializer(photo)
            if serializer:
                return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# //////////////////////////////////////////////////////////////////#
class UserPicturesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserPicturesModel.objects.all()
    serializer_class = UserPicturesSerializer

    def update(self, request, *args, **kwargs):
        if request.method == "PUT" or request.method == "PATCH":
            return JsonResponse(
                {"detail": 'Method "PUT" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            partial = kwargs.pop("pk")

            Picture = UserPicturesModel.objects.filter(id=partial)
            if len(Picture):
                path = str(
                    UserPicturesModel.objects.all().get(id=partial).profile_photo
                )
                if path == "/static/blank_profile_image.png":
                    Picture.delete()
                else:
                    fs = FileSystemStorage()
                    fs.delete(path)
                    Picture.delete()
                return response.HttpResponse(status=status.HTTP_204_NO_CONTENT)
            return JsonResponse(
                {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )


# //////////////////////////////////////////////////////////////////#
class UserSearchView(APIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            try:
                username = request.data["username"]
            except KeyError:
                return JsonResponse(
                    {
                        "username": "KeyError search key ('username') is missing which should be in form-data"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            users = UserModel.objects.filter(Q(username__icontains=username))
            if not len(users):
                return JsonResponse(
                    {"user": f"No matching users for {username}"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            serializer = UserModelSerializer(users, many=True)
            return JsonResponse(
                data=serializer.data, safe=False, status=status.HTTP_200_OK
            )


# //////////////////////////////////////////////////////////////////#
class UserFollower(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            try:
                user = request.data["user"]
            except:
                return JsonResponse(
                    {
                        "user": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not user:
                return JsonResponse(
                    {
                        "user": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            try:
                user = UserModel.objects.get(pk=user)
            except:
                return JsonResponse(
                    {
                        "user": f"UserModel with ID: {user} doesn't exist.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

            main_user = UserModel.objects.get(pk=request.user.id)

            is_follows = False
            for follow in main_user.follows.all():
                if follow == user:
                    is_follows = True
                    break

            if not is_follows:
                main_user.follows.add(user)
                user.followers.add(main_user)
                Notification.objects.create(
                    notification_type=5, to_user=user, from_user=main_user
                )

            if is_follows:
                main_user.follows.remove(user)
                user.followers.remove(main_user)
                Notification.objects.create(
                    notification_type=6, to_user=user, from_user=main_user
                )
            return JsonResponse({"detail": "ok"}, status=status.HTTP_200_OK)


# //////////////////////////////////////////////////////////////////#
class UserSetPasswordView(APIView):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            try:
                email = request.data["email"]
            except:
                return JsonResponse(
                    {
                        "email": "this feild is requierd",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not email:
                return JsonResponse(
                    {
                        "email": "This field may not be blank.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            if not (re.fullmatch(regex, email)):
                return JsonResponse(
                    {
                        "email": "please enter a valid email address.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            try:
                user = UserModel.objects.all().filter(email=email)
                username = UserModel.objects.all().get(email=email).username
            except:
                return JsonResponse(
                    {
                        "email": f"{email} does not exist, please enter the correct email address.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            if not len(user):
                return JsonResponse(
                    {
                        "email": "please enter the correct email address.",
                    },
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )
            password_mok = "QqWwEeRrTtYyUu$&*IiOoPpAaSsDdFfG01234gHhJjKkLlZzXxCcVvBbNnMm56789!@#QqWwEeSsDdFfG012RrTtYyUu$&*IiOoPpAa34gHhJjKkLlZz!@#XxCcVvBbNnMm56789"
            set_password = "".join(random.sample(password_mok, 10))
            new_password = make_password(set_password)
            user.update(password=new_password)
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("tellxus.app@gmail.com", "qw1qw2qw3")
            server.sendmail(
                "tellxus.app@gmail.com",
                f"{email}",
                f"Hey {username}! \nThank you for using TellXUs app \nyour new password is successfully created. \nPassword: {set_password}",
            )

            return JsonResponse(
                {
                    "password": f"Password was successfully reset 👍.\n we sent the new password to {email} user",
                },
                status=status.HTTP_200_OK,
            )


# //////////////////////////////////////////////////////////////////#
# class ThreadModelPostView(ListCreateAPIView):
#     queryset = ThreadModel.objects.all()
#     serializer_class = ThreadModelSerializer

#     def post(self, request, *args, **kwargs):
#         if request.method == "POST":
#             partial = kwargs.pop("pk")
#             try:
#                 receiver = UserModel.objects.get(pk=partial)
#             except:
#                 return JsonResponse(
#                     {
#                         "receiver": f"receiver with ID: {partial} doesn't exist.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             sender = request.user

#             if sender == receiver:
#                 return response.HttpResponse(status=status.HTTP_406_NOT_ACCEPTABLE)

#             if (
#                 not ThreadModel.objects.all()
#                 .filter(sender=sender, receiver=receiver)
#                 .exists()
#             ):
#                 if (
#                     not ThreadModel.objects.all()
#                     .filter(sender=receiver, receiver=sender)
#                     .exists()
#                 ):
#                     thread = ThreadModel.objects.create(
#                         sender=sender, receiver=receiver
#                     )
#                     thread.save()
#                     return JsonResponse(
#                         {"detail": "ok"}, status=status.HTTP_201_CREATED
#                     )
#                 return JsonResponse(
#                     {"thread": "thread is already exist."}, status=status.HTTP_200_OK
#                 )
#             return JsonResponse(
#                 {"thread": "thread is already exist."}, status=status.HTTP_200_OK
#             )

#     def get(self, request, *args, **kwargs):
#         if request.method == "GET":

#             threads = ThreadModel.objects.all().filter(
#                 Q(sender=request.user) | Q(receiver=request.user)
#             )
#             if threads:
#                 serializer = ThreadModelSerializer(threads, many=True)
#                 if serializer:
#                     return JsonResponse(
#                         serializer.data, safe=False, status=status.HTTP_202_ACCEPTED
#                     )
#                 return JsonResponse(
#                     serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
#                 )
#             return JsonResponse(
#                 {"threads": "There are no conversations yet."},
#                 status=status.HTTP_200_OK,
#             )


# # //////////////////////////////////////////////////////////////////#
# class ThreadModelDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = ThreadModel.objects.all()
#     serializer_class = ThreadModelSerializer

#     def get(self, request, *args, **kwargs):
#         if request.method == "GET":
#             return JsonResponse(
#                 {"detail": 'Method "GET" not allowed.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )

#     def update(self, request, *args, **kwargs):
#         if request.method == "PUT" or request.method == "PATCH":
#             return JsonResponse(
#                 {"detail": 'Method "PUT" not allowed.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )


# # //////////////////////////////////////////////////////////////////#
# class MessageModelPostView(ListCreateAPIView):
#     queryset = MessageModel.objects.all()
#     serializer_class = MessageModelSerializer

#     def get(self, request, *args, **kwargs):

#         partial = kwargs.pop("pk")
#         if request.method == "GET":
#             try:
#                 thread = ThreadModel.objects.get(pk=partial)
#             except:
#                 return JsonResponse(
#                     {
#                         "thread": f"ThreadModel with ID: {partial} doesn't exist.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             massages = MessageModel.objects.all().filter(thread=thread)
#             if massages:
#                 serializer = MessageModelSerializer(massages, many=True)
#                 if serializer:
#                     return JsonResponse(
#                         serializer.data, safe=False, status=status.HTTP_200_OK
#                     )
#                 return JsonResponse(
#                     serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST
#                 )
#             return JsonResponse(
#                 {"massages": "There are no messages on this conversation yet."},
#                 status=status.HTTP_204_NO_CONTENT,
#             )

#     def post(self, request, *args, **kwargs):
        
#         partial = kwargs.pop("pk")
#         if request.method == "POST":
#             try:
#                 thread = ThreadModel.objects.get(pk=partial)
#             except:
#                 return JsonResponse(
#                     {
#                         "thread": f"ThreadModel with ID: {partial} doesn't exist.",
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             receiver_user = thread.receiver if request.user == thread.sender else thread.sender
#             print(request.user,receiver_user)
