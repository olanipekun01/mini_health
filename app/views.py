from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from app.models import User, Patient, CaseFolder, MedicalHistory, DiagnosisAdmission, VitalSigns, PatientNote
from app.serializers import *
from app.permissions import IsHIMRole, IsNurseRole, IsDoctorRole, IsHIMOrDoctorRole, IsNurseOrDoctorRole, IsHIMNurseOrDoctorRole

from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.http import Http404



class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        is_superuser = serializer.validated_data.get('is_superuser', False)
        is_staff = serializer.validated_data.get('is_staff', False)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data['username'])

        if user.is_authorized:
            response_data = serializer.validated_data
            response_data['detail'] = "Logged in successfully."
            refresh = RefreshToken.for_user(user)
            user.refresh_token = str(refresh)
            user.save()

            response = Response(response_data, status=status.HTTP_200_OK)
            # response.set_cookie('login_status', 'success', secure=True, samesite='None')
            response.set_cookie('refreshToken', user.refresh_token, secure=True, samesite='None')

            return response
        else:
            return Response({"detail": "Your account has not been approved by an admin yet."}, status=status.HTTP_200_OK)



class LogoutAPIView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = LogoutSerializer
    @permission_classes([AllowAny])
    # permission_classes = (permissions.ISAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class TokenLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        token = request.data.get('token')

        user = User.objects.filter(username=username, login_token=token).first()
        if user is not None:
            # the token is correct. You can log in the user here.
            user.login_token = None # clear the token
            user.save()

            response = Response({'detail': "Logged in successfully."}, status=status.HTTP_200_OK)
            # response.set_cookie('refreshToken', token.refreshToken, secure=True, samesite='None')
            response.set_cookie('refreshToken', user.tokens.refresh, secure=True, samesite='None')

            return response
        else:
            return Response({'detail': "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

# class PasswordResetOTPEmailView(generics.CreateAPIView):
#     serializer_class = PasswordResetSerializer


#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data['email']
#         data = serializer.save()

#         # Generate a unique confirmation URL for your local server
#         confirmation_url_password_reset = f'http://localhost:8000/reset-password-confirmation/?email={email}&otp={data["otp"]}'


#         #send and email with OTP and the confirmation link
#         subject = 'Password Reset OTP and Confirmation Link'
#         message = f'Use this OTP to reset your password: {data["otp"]}\n\n'
#         message += f'\n\nAlternatively, you can click on the link below to reset your password: \n{confirmation_url_password_reset}'


#         from_email = 'webmaster@example.com'
#         recipient_list = [email]

#         send_mail(subject, message, from_email, recipient_list)

#         return Response({'message': 'Password reset OTP and confirmation link sent successfully.'}, status=status.HTTP_200_OK)

# class PasswordResetConfirmationView(DetailView):
#     model = User
#     template_name = 'password_reset_confirmation.html'
#     context_object_name = 'user'


#     def get_object(self, queryset=None):
#         email = self.request.GET.get('email')
#         otp = self.request.GET.get('otp')

#         if not email or not otp:
#             raise Http404("Invalid URL")

#         user = User.objects.filter(email=email, login_token=otp).first()

#         if user is None:
#             raise Http404("Invalid OTP")
        
#         return user

#     def post(self, request, *args, **kwargs):
#         user = self.get_object()
#         new_password = request.POST.get('password')

#         # set the new password
#         user.set_password(new_password)
#         user.save()

#         messages.success(request, 'Password reset successfully.')
#         return redirect('app:login')


# Create your views here.
# @api_view(['POST'])
# @permission_classes([permissions.AllowAny])
# def login_user(request):
#     """Login user and return JWT tokens"""
#     username = request.data.get('username')
#     password = request.data.get('password')
    
#     if username and password:
#         user = authenticate(username=username, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'Login successful',
#                 'user': {
#                     'id': user.id,
#                     'username': user.username,
#                     'role': user.role,
#                     'first_name': user.first_name,
#                     'last_name': user.last_name,
#                 },
#                 'tokens': {
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

