import requests
from django.shortcuts import render
from django.middleware import csrf
from django.middleware.csrf import get_token
from django.contrib import auth
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.conf import settings
from django.utils.decorators import method_decorator


import json

#from jwcrypto import jwt
from rest_framework.response import Response
from rest_framework import status, response, views, viewsets, generics, exceptions as rest_exceptions, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import views as jwt_views, tokens, serializers as jwt_serializers, exceptions as jwt_exceptions
# Create your views here.

from .models import CustomUserModel
from .serializers import UsersSerializer


class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):

    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            token = jwt_exceptions.InvalidToken("No valid token found in cookie \'refresh\'")
            return token


class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]
            )

            del response.data["refresh"]

        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)



class SignUpView(views.APIView):
    
    permission_classes = (rest_permissions.AllowAny, )

    def post(self, request, format=None):
        
        data = request.data

        username = data["username"]
        password = data["password"]
        re_password = data["re_password"]
        email = data["email"]

        
        if password == re_password:
            if CustomUserModel.objects.filter(email=email).exists():
                return Response({"err": "A user with this email already exists"}, status.HTTP_400_BAD_REQUEST)

            elif CustomUserModel.objects.filter(username=username).exists():
                return Response({"err": "A user with this username already exists"})

            else:

                if len(password) < 6:
                    return Response({"err": "the password must've at least 6 characters"}, status.HTTP_400_BAD_REQUEST)

                else:

                    CustomUserModel.objects.create_external_user(username=username, password=password, email=email)
                    ## TESTE
                    #CustomUserModel.objects.create_superuser(username=username, password=password, email=email)

                    return Response({"success": "A user was successfully created"}, status.HTTP_200_OK)

        return Response({"err": "something went wrong trying create a new user"})
        
        
        


def get_user_token(u):
    refresh = tokens.RefreshToken.for_user(u)

    return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token)
        }


class LoginView(views.APIView):
    permission_classes = (rest_permissions.AllowAny, )

    def post(self, request, format=None):

        data = request.data

        username = data["username"]
        password = data["password"]

        if not password:
            return Response({"err": "password is required for login"}, status.HTTP_400_BAD_REQUEST)

        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                tokens = get_user_token(user)
                auth.login(request, user)
                res = Response()

                res.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=tokens["access_token"],
                    expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]

                )

                res.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"],
                    value=tokens["refresh_token"],
                    expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"]

                )

                res.data = tokens

                res["X-CSRFToken"] = csrf.get_token(request)

                return res

            else:
                return Response({"err": "error trying authenticating"}, status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"err": "something went wrong"}, status.HTTP_400_BAD_REQUEST)


class CheckAuthenticated(views.APIView):

    def get(self, request, format=None):
        user = self.request.user

        try:
            isUserAuthenticated = user.is_authenticated

            if isUserAuthenticated:
                return Response({"authenticated": True}, status.HTTP_200_OK)

            else:
                return Response({"authenticated": False}, status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"err": "something went wrong when checking authentication status"}, status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):

    def post(self, request, *args, **kwargs):

        try:
            auth.logout(request)

            refreshToken = request.COOKIES.get(
                settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"]
            )

            token = tokens.RefreshToken(refreshToken)
            token.blacklist()

            res = response.Response()
            res.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
            res.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH"])
            res.delete_cookie("X-CSRFToken")
            res["X-CSRFToken"] = None

            return res

        except:
            return Response({"err": "failed to logout"}, status.HTTP_400_BAD_REQUEST)


@rest_decorators.api_view(["GET"])
@rest_decorators.permission_classes([rest_permissions.IsAuthenticated])
def user(request):
    try:
        user = CustomUserModel.objects.get(id=request.user.id)
    except:

        return Response({"err": "Failed to retrieve user"}, status.HTTP_400_BAD_REQUEST)

    serializer = UsersSerializer(user)

    return Response(serializer.data)

