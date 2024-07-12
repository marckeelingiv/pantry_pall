from django.db.models import Q
from django.conf import settings
from accounts.serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    EmailVerifySerializer, 
    UserProfileSerializer, 
    ChangePasswordSerializer
)
from accounts.models import CustomUser
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        first_name = serializer.data.get('name')
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        if CustomUser.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists():
            return Response({'message': 'Email Already Exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=email, email=email, password=password, first_name=first_name)
        confirmation_token = default_token_generator.make_token(user)
        activation_link = f'{settings.FRONT_END}api/v1/accounts/verify?user_id={user.id}&confirmation_token={confirmation_token}'
        print(activation_link)  # Consider logging instead of print in production

        message_content = f"Simply click the link below to verify your account.<br /><br />{activation_link}"
        subject = 'Account Verification on ....'
        message = render_to_string('notification.html', {"message": message_content, "name": first_name})

        # Uncomment and configure email sending with SendGrid or another email service
        # try:
        #     message = Mail(from_email=From("info@yourdomain.com", "Your Project Name"), to_emails=user.email, subject=subject, html_content=message)
        #     sg = SendGridAPIClient(settings.SENDGRID_KEY)
        #     response = sg.send(message)
        # except Exception as e:
        #     return Response({'message': "Unable to send verification Email"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': f'Account successfully created, We have sent you a verification email to {email}. Click on the link in the email to activate your account.',
            'user': user.id
        }, status=status.HTTP_200_OK)

class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = authenticate(username=email, password=password)
        if user:
            if user.is_verify:
                token = RefreshToken.for_user(user)
                return Response({
                    'username': user.username,
                    'first_name': user.first_name,
                    'email': user.email,
                    'token': str(token.access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Please verify your email then try again'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailAPIView(generics.CreateAPIView):
    serializer_class = EmailVerifySerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.data.get('user_id')
        confirmation_token = serializer.data.get('confirmation_token')

        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, confirmation_token):
            return Response({'message': 'Token is invalid or expired. Please request another confirmation email.'}, status=status.HTTP_400_BAD_REQUEST)
        elif user.is_verify:
            return Response({'message': "Your Email is already verified"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_verify = True
            user.save()

        return Response({'message': 'Email Successfully Verified'}, status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class ChangePasswordAPIView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.object.check_password(serializer.data.get("old_password")):
            return Response({'message': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)

        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()

        return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
