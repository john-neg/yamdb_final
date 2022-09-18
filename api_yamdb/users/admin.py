from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'role',
        'email',
        'confirmation_code',
        'is_active',
        'is_superuser',
    ]


admin.site.register(User, UserAdmin)
