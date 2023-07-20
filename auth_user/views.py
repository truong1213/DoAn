from django.shortcuts import render
from rest_framework.generics import CreateAPIView,UpdateAPIView
from .models import CustomUser,TokenRegister,TokenResetPassword
from .serializers import CustomUserSerializer,TokenRegisterSerializer,ChangePasswordSerializer,TokenResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.
class Register(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False) 
        token = TokenRegister.objects.create(email=user)
        serializer_token = TokenRegisterSerializer(token)
        html = render_to_string('auth_user/VerifyEmail.html',{'token':serializer_token.data['token']})
        send_mail(
                subject='',
                html_message=html,
                message=html,
                fail_silently=False,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email,],
            )
        return JsonResponse(data={"message":"success"})
class ResendMail(CreateAPIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email']
        ),
        responses={
            200: 'OK',
            400: 'Bad Request',
            404: 'Not Found',
        }
    )
    def post(self, request):
        email = request.data['email']
        user = CustomUser.objects.filter(email=email).first()
        print(user.is_active)
        if user is not None:
            if user.is_active==False:
                time_now = datetime.now()
                TokenRegister.objects.filter(email=user,create_at__lt = time_now).delete()
                token = TokenRegister.objects.create(email=user)
                serializer = TokenRegisterSerializer(token)
                html = render_to_string('auth_user/VerifyEmail.html',{'token':serializer.data['token']})
                send_mail(
                            subject='',
                            html_message=html,
                            message=html,
                            fail_silently=False,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[user.email],
                        )
                return JsonResponse({"message":"success"})
            else:
                return JsonResponse({"message":"Tài khoản đã được xác nhận"})
        else:
            return JsonResponse({"message":'Tài khoản không tồn tại'})
class RegisterComplete(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_PATH,
                description='Token',
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description='Success',
                examples={
                    'application/json': {
                        'message': 'success'
                    }
                }
            ),
            400: openapi.Response(
                description='Failed',
                examples={
                    'application/json': {
                        'message': 'failed'
                    }
                }
            )
        }
    )
    def get(self, request, token):
        token_obj = TokenRegister.objects.filter(token=token).first()
        if token_obj:
            email = token_obj.email
            user = CustomUser.objects.filter(email=email).first()
            user.is_active = True
            user.save()
            token_obj.delete()
            TokenRegister.objects.filter(email=email).delete()
            return JsonResponse({"message":"success"})
        else:
            return JsonResponse({"message":"failed"})
class ChangePassword(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user_email = request.user
        user = CustomUser.objects.filter(email=user_email).first()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data.get('password'))
            user.save()
            return JsonResponse({"message":"success"})
        else:
            return JsonResponse({"message":"failed"})
class ResetPassword(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: 'Password reset email sent successfully',
            400: 'User account not found',
        },
    )
    def post(self, request):
        email = request.data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user:
            TokenResetPassword.objects.create(email=user)
            token = TokenResetPassword.objects.filter(email=user).first()
            serializer = TokenResetPasswordSerializer(token)
            html = render_to_string('auth_user/sendmailresetpassword.html',{"token":serializer.data['token']})     
            send_mail(
                subject="mail reset password",
                message=html,
                html_message=html,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently=False,
            )
            return JsonResponse({"message":'Check mail'})
        else:
            return JsonResponse(data={'message':"Tài khoản chưa đăng kí"})
class ResetPasswordConfirm(UpdateAPIView):
    queryset = TokenResetPassword.objects.all()
    serializer_class = ChangePasswordSerializer
    def get(self, request, token):
        print(token)
        token_obj = TokenResetPassword.objects.filter(token=token).first()
        if token_obj:
            return JsonResponse({"token":1})
        else:
            return JsonResponse({"token":None})
    def patch(self, request,token):
        token_obj = TokenResetPassword.objects.filter(token=token).first()
        passwordnew = request.data['password']
        if token_obj:
            email = token_obj.email
            user = CustomUser.objects.filter(email=email).first()   
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.data.get('password'))
                user.save()
                TokenResetPassword.objects.filter(email=user).delete()
                return JsonResponse({"message":"success"})
            else:
                return JsonResponse({"message":"failed"})
        else:
            return JsonResponse({"message":"failed"})