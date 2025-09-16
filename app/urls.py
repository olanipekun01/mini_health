from . import views
from django.urls import path, include

from rest_framework_simplejwt.views import ( TokenRefreshView, )

app_name = 'app'

# from .views import (
#     PasswordResetOTPEmailView,
#     PasswordResetConfirmationView,
# )

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #password reset
#     path('reset-password-email/', PasswordResetOTPEmailView.as_view(), name='reset-password-email'),
#     path('reset-password-confirmation/', PasswordResetConfirmationView.as_view(), name='reset-passsword-confirmation'),
]