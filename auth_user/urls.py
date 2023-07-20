from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
 TokenObtainPairView,
 TokenRefreshView,
)
urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('register-resendmail/',views.ResendMail.as_view(),name="resendmail"),
    path('register-complete/<token>',views.RegisterComplete.as_view(),name="registercomplete"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/',views.ChangePassword.as_view(),name="changepassword"),
    path('reset-password/',views.ResetPassword.as_view(),name="resetpassword"),
    path('reset-password-confirm/<token>',views.ResetPasswordConfirm.as_view()),
]