from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("user", views.user),
    path("refresh-token", views.CookieTokenRefreshView.as_view()),
    path("logout", views.LogoutView.as_view()),
    
]