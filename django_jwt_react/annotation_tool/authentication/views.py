import os
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template
from django.views import View
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .send_email import EmailAlert
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from .models import CustomUser


class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        # print(request.data['email']+","+request.data["username"])
        # return Response(request.data, status=status.HTTP_201_CREATED)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                print(user.pk)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                print(uidb64)
                id = force_text(urlsafe_base64_decode(uidb64))
                print(id)
                domain = get_current_site(request).domain
                token = account_activation_token.make_token(user)
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
                activation_link = 'http://' +domain+ link
                content = {"user": user.username, "link": activation_link}
                #print(activation_link)
                activation_alert = EmailAlert(request.data['email'], request.data["username"],content)
                activation_alert.send_activation_email()
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):

        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(View):
    def get(self, request):
        cwd = os.path.abspath(os.getcwd())
        #template_path = cwd=os.path.abspath(os.getcwd())
        template_path=os.path.abspath(os.path.join(cwd, os.pardir))+"/annotation_tool/frontend/templates/frontend/index.html"
        return redirect('/sign-in')


class ActivationView(View):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    def get(self, request, uidb64, token):
        print(uidb64)
        id = force_text(urlsafe_base64_decode(uidb64))
        print(id)
        cwd = os.path.abspath(os.getcwd())
        template_path = cwd = os.path.abspath(os.getcwd())
        template_path = os.path.abspath(
        os.path.join(cwd, os.pardir)) + "/annotation_tool/frontend/templates/frontend/index.html"
        user = CustomUser.objects.get(pk=id)
        if ((not account_activation_token.check_token(user, token)) or user.is_active):
            return redirect('/')

           # return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        user.is_active = True
        user.save()
        return render(request, template_path)
        #return Response(status=status.HTTP_200_OK)



class ChangePassword(APIView):
    # permission_classes = (permissions.AllowAny,)
    # authentication_classes = ()

    def post(self, request):
        try:
            given_email = request.data["email"]
            user = CustomUser.objects.get(email=given_email)
            data={"email":given_email,"password":request.data['old_password']}
            r=requests.post("http://127.0.0.1:8000/api/token/obtain/",data =data)
            if (r.status_code==200) :
                user.set_password(request.data["new_password"])
                user.save()
                #return Response(data={"textmessage": "Password changed succcessfully"}, status=status.HTTP_200_OK)
                return Response(data={"code": 1}, status=status.HTTP_200_OK)
            else:
                return Response(data={"code": 0}, status=status.HTTP_200_OK)
               # return Response(data={"textmessage": "Wrong Password"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(data={"code": 0}, status=status.HTTP_200_OK)
           # return Response(status=status.HTTP_400_BAD_REQUEST)

class ResetPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()


    def post(self,request):
     try:
        given_email=request.data["email"]
        user=CustomUser.objects.get(email=given_email)
        password=CustomUser.objects.make_random_password()
        user.set_password(password)
        user.save()
       # print("pass1:"+password)
        content={"user":user.username,"password":password}
        reset_alert = EmailAlert(given_email, user.username, content)
        reset_alert.send_resetpassword_email()
        return Response(data={"code": 1}, status=status.HTTP_200_OK)
       # return Response(data={"textmessage": "Reset Password success.Look your email"}, status=status.HTTP_200_OK)
     except Exception as e:
         return Response(data={"code": 0}, status=status.HTTP_200_OK)
       #return Response(data={"textmessage": "There is not account with this email"},status=status.HTTP_400_BAD_REQUEST)

# from pathlib import Path
# from email.mime.image import MIMEImage
# from django.core.mail import EmailMultiAlternatives
# class TestView(APIView):
#     permission_classes = (permissions.AllowAny,)
#
#     authentication_classes = ()
#     def get(self,request):
#         recipient = "ece7866@upnet.gr"
#         sender = "no-reply@ellogon.gr"
#         image_path = '/home/alex/PycharmProjects/django_jwt_react/django_jwt_react/annotation_tool/frontend/static/frontend/images/EllogonCyan.png'
#         image_name = Path(image_path).name
#         subject = "Reset Password."
#         text_message = f"This is an automatic email from {sender}.Please don't reply"
#         cwd = os.path.abspath(os.getcwd())
#         template_path = os.path.abspath(
#         os.path.join(cwd, os.pardir)) + "/annotation_tool/frontend/templates/frontend/reset_password.html"
#         content={"user":"ece7866","password":"12345678"}
#         html_message = get_template(template_path).render(content)
#         html_message=str(html_message).format(image_name=image_name)
#     #     html_message="""
#     # <!doctype html>
#     #     <html lang=en>
#     #         <head>
#     #             <meta charset=utf-8>
#     #             <title>Some title.</title>
#     #         </head>
#     #         <body>
#     #             <h1>{subject}</h1>
#     #             <p>
#     #             Here is my nice image.<br>
#     #             <img src='cid:{image_name}'/>
#     #             </p>
#     #         </body>
#     #     </html>
#     # """.format(subject=subject,image_name=image_name)
#     #     html_message = f"""
#     # <!doctype html>
#     #     <html lang=en>
#     #         <head>
#     #             <meta charset=utf-8>
#     #             <title>Some title.</title>
#     #         </head>
#     #         <body>
#     #             <h1>{subject}</h1>
#     #             <p>
#     #             Here is my nice image.<br>
#     #             <img src='cid:{image_name}'/>
#     #             </p>
#     #         </body>
#     #     </html>
#     # """
#         print(type(html_message))
#         email = EmailMultiAlternatives(subject=subject, body=text_message, from_email=sender,
#                                    to=[recipient])
#         email.attach_alternative(html_message, "text/html")
#         email.content_subtype = 'html'
#         email.mixed_subtype = 'related'
#         with open(image_path, mode='rb') as f:
#             image = MIMEImage(f.read())
#             email.attach(image)
#             image.add_header('Content-ID', f"<{image_name}>")
#         email.send()
#         return Response( status=status.HTTP_200_OK)

class MainView(APIView):

    def get(self, request):

        return Response(data={"hello": "world"}, status=status.HTTP_200_OK)

class ManageProfileView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)