from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'last_name', 'phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'last_name', 'phone_number', 'is_staff')
    search_fields = ('email', 'name', 'last_name', 'phone_number')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
