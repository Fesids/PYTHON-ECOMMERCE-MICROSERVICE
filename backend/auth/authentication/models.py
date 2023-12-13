from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
import uuid
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, email, password):

        if not email:
            raise ValueError("A user must've a email")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, email, password):

        if not email:
            raise ValueError("A superuser must've an email")

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save()

        return user

    def create_employee_user(self, username, email, password):
        if not email:
            raise ValueError("A user must've an email")

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = False
        user.is_external = False

        user.save()

        return user

    def create_external_user(self, username, email, password):

        if not email:
            raise ValueError("A user must've an email")

        user = self.create_user(username, email, password)
        user.is_staff= False
        user.is_superuser= False
        user.is_external=True

        user.save()

        return user


class CustomUserModel(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=244, unique=True)
    username = models.CharField(max_length=244, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_external = models.BooleanField(default=False)
    #jwt_secret = models.UUIDField(default=uuid.uuid4)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def jwt_get_secret_key(self):
        return self.jwt_secret