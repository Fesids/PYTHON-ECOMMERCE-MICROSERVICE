from django.contrib import admin
from .models import CustomUserModel
# Register your models here.


@admin.register(CustomUserModel)
class UserAdmin(admin.ModelAdmin):
    fields = ["username", "email"]
