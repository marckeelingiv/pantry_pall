from django.urls import path
from . import views
urlpatterns = [

    path('login/', views.LoginAPIView.as_view(), name="login_user"),
    path('signup/', views.RegisterAPIView.as_view(), name="signup_user"),
    path('user/', views.UserRetrieveUpdateAPIView.as_view(), name='user_account'),
    path('verify/', views.VerifyEmailAPIView.as_view(), name='verfiy_email'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name="change_password"),

]