import shutil, os, random, re, requests
from django.http import JsonResponse, response
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from Articles_API.models import Notification

from .models import UserModel, UserPicturesModel  # , MessageModel, ThreadModel

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
                    status=status.HTTP_400_BAD_REQUEST,
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
                    status=status.HTTP_400_BAD_REQUEST,
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
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {
                "username": username,
                "email": email,
                "password": password,
            }

            try:
                gender = request.data["gender"]
            except:
                gender = False

            try:
                city = request.data["city"]
            except:
                city = False

            try:
                birth_date = request.data["birth_date"]
            except:
                birth_date = False

            try:
                bio = request.data["bio"]
            except:
                bio = False

            if bio:
                data["bio"] = bio

            if birth_date:
                data["birth_date"] = birth_date

            if gender:
                data["gender"] = gender

            if city:
                data["city"] = city

            try:
                profile_photo = request.data["profile_photo"]
                if not len(profile_photo):
                    profile_photo = "/static/blank_profile_image.png"
            except:
                profile_photo = "/static/blank_profile_image.png"

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

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            if request.user.is_anonymous:
                return JsonResponse(
                    {"detail": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED
                )
            partial = request.user.id
            print(request.user)
            user = UserModel.objects.get(pk=partial)
            serializer = UserModelSerializer(user)
            if serializer:
                return JsonResponse(serializer.data, status=status.HTTP_202_ACCEPTED)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.method == "PATCH":
            return JsonResponse(
                {"detail": '"PATCH" requests not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        if request.method == "PUT":

            partial = request.user.id

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
                except:
                    pass

                try:
                    email = request.data["email"]
                    if email:

                        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
                        if not (re.fullmatch(regex, email)):
                            return JsonResponse(
                                {
                                    "email": "please enter a valid email format.",
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
                except:
                    pass

                try:
                    password = request.data["password"]
                    if password:
                        new_password = make_password(password)
                        user.update(password=new_password)
                except:
                    pass

                try:
                    gender = request.data["gender"]
                    if gender:
                        user.update(gender=gender)
                except:
                    pass

                try:
                    city = request.data["city"]
                    if city:
                        user.update(city=city)
                except:
                    pass

                try:
                    birth_date = request.data["birth_date"]
                    if birth_date:
                        user.update(birth_date=birth_date)
                except:
                    pass

                try:
                    bio = request.data["bio"]
                    if bio:
                        user.update(bio=bio)
                except:
                    pass

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
            partial = request.user.id
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

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            return JsonResponse(
                {"detail": 'Method "GET" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

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

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            partial = kwargs.pop("pk")
            Pictures = UserPicturesModel.objects.all().filter(user_id=partial)
            if len(Pictures):
                serializer = UserPicturesSerializer(Pictures, many=True)
                return JsonResponse(
                    data=serializer.data,
                    safe=False,
                    status=status.HTTP_200_OK,
                )
            else:
                return JsonResponse(
                    {"detail": "NO_CONTENT"}, status=status.HTTP_204_NO_CONTENT
                )

    def update(self, request, *args, **kwargs):
        if request.method == "PUT" or request.method == "PATCH":
            return JsonResponse(
                {"detail": 'Method "PUT" not allowed.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            partial = kwargs.pop("pk")
            user_Pictures = UserPicturesModel.objects.filter(user_id=request.user.id)
            if len(user_Pictures) == 1:
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
                    photo = UserPicturesModel.objects.create(user_id=request.user)
                    photo.save()
                    return response.HttpResponse(status=status.HTTP_204_NO_CONTENT)
                return JsonResponse(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )
            else:
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
class GetUserFollowers(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            if request.user.is_anonymous:
                return JsonResponse(
                    {"detail": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                user_followers = []
                user_id = request.user.id
                main_user = UserModel.objects.get(pk=user_id)
                if len(main_user.followers.all()):
                    for user in main_user.followers.all():
                        user = UserModel.objects.get(pk=user)
                        user_pic = "/media/" + str(
                            UserPicturesModel.objects.all()
                            .filter(user_id=user)
                            .last()
                            .profile_photo
                        )
                        user_followers.append(
                            {
                                "id": user.id,
                                "username": user.username,
                                "user_pic": user_pic,
                            }
                        )
                    return JsonResponse(
                        user_followers, safe=False, status=status.HTTP_200_OK
                    )
                else:
                    return JsonResponse(
                        user_followers, safe=False, status=status.HTTP_204_NO_CONTENT
                    )


# //////////////////////////////////////////////////////////////////#
class GetUserFollows(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            if request.user.is_anonymous:
                return JsonResponse(
                    {"detail": "UNAUTHORIZED"}, status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                user_follows = []
                user_id = request.user.id
                main_user = UserModel.objects.get(pk=user_id)
                if len(main_user.follows.all()):
                    for user in main_user.follows.all():
                        user = UserModel.objects.get(pk=user)
                        user_pic = "/media/" + str(
                            UserPicturesModel.objects.all()
                            .filter(user_id=user)
                            .last()
                            .profile_photo
                        )
                        user_follows.append(
                            {
                                "id": user.id,
                                "username": user.username,
                                "user_pic": user_pic,
                            }
                        )
                    return JsonResponse(
                        user_follows, safe=False, status=status.HTTP_200_OK
                    )
                else:
                    return JsonResponse(
                        user_follows, safe=False, status=status.HTTP_204_NO_CONTENT
                    )


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
                        "email": "please enter a valid email format.",
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

            subject, from_email, to = (
                "New Password",
                settings.EMAIL_HOST_USER,
                f"{email}",
            )
            text_content = f"Hey {username}!"

            html_content = f"""<div style="border-style:solid;border-width:thin;border-color:#dadce0;border-radius:8px;padding:40px 20px" align="center" class="m_-3214643286528040867mdv2rw"><img src="https://i.ibb.co/DbvpHh4/logo-text.png" width="74" height="24" aria-hidden="true" style="margin-bottom:16px" alt="TellXus" class="CToWUd"><div style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;border-bottom:thin solid #dadce0;color:rgba(0,0,0,0.87);line-height:32px;padding-bottom:24px;text-align:center;word-break:break-word"><div style="font-size:24px">App password created to sign in to your account </div><table align="center" style="margin-top:8px"><tbody><tr style="line-height:normal"><td align="right" style="padding-right:8px"></td><td><a style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;color:rgba(0,0,0,0.87);font-size:14px;line-height:20px"><strong>{email}</strong></a></td></tr></tbody></table> </div><div style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:14px;color:rgba(0,0,0,0.87);line-height:20px;padding-top:20px;text-align:center">If you didn't generate this password for your account, someone might be using your account. Check and secure your account now.
            <strong>or</strong> you can reply to this email to make a ticket for your issue, the technical support will contact you asap.<div style="padding-top:32px;text-align:center"><div  style="font-family:'Google Sans',Roboto,RobotoDraft,Helvetica,Arial,sans-serif;line-height:20px;color:#303030;font-weight:500;text-decoration:none;font-size:20px;display:inline-block;padding:10px 24px; background-color:#dadada;border-radius:5px;min-width:90px" >{set_password}</div></div></div><span class="im"><div style="padding-top:20px;font-size:12px;line-height:16px;color:#5f6368;letter-spacing:0.3px;text-align:center">Thank you for using TellXus<br><a style="color:rgba(0,0,0,0.87);text-decoration:inherit" href="https://TellXus.com">TellXus.com</a></div></span></div>"""

            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse(
                {
                    "password": f"Password was successfully reset 👍. we sent the new password to {email}, please check your spam if you don't receive it in your inbox.",
                },
                status=status.HTTP_200_OK,
            )


# //////////////////////////////////////////////////////////////////#
class EmailStatus(APIView):
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            # check for required Params.
            try:
                to_email = request.GET["to_email"]
            except:
                return JsonResponse(
                    {
                        "to_email": "KeyError! search key ('to_email') is missing which should be in the Query Params"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # check email format.
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            if not (re.fullmatch(regex, to_email)):
                return JsonResponse(
                    {
                        "detail": "Waiting for a valid email format.",
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            # Check if the received email is reachable and accepts mail by calling Reacher's third-party API.
            url = "https://api.reacher.email/v0/check_email"
            headers = {"authorization": "50dfea0a-a3f3-11ec-95af-1935d61c5545"}
            payload = {"to_email": f"{to_email}"}
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            # check requests rate
            if data["error"] and "Too many requests" in data["error"]:
                error = data["error"]
                return JsonResponse(
                    {
                        "detail": f"{error}",
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            is_reachable = (
                data["is_reachable"] != "invalid" and data["is_reachable"] != "unknown"
            )
            accepts_mail = data["mx"]["accepts_mail"]
            is_accepted = accepts_mail and is_reachable
            return JsonResponse(
                {"detail": f"{'acepted' if is_accepted else 'rejected'}"},
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

# def get(self, request, *args, **kwargs):
#     if request.method == "GET":
#         return JsonResponse(
#             {"detail": 'Method "GET" not allowed.'},
#             status=status.HTTP_405_METHOD_NOT_ALLOWED,
#         )

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
