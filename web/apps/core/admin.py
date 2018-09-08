from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.core.models import PUUser

class UserAdmin(UserAdmin):
    pass
admin.site.register(PUUser, UserAdmin)
