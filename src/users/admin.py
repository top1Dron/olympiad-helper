from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'username',)
    list_filter = ('email', 'is_staff', 'is_active', 'username',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'username',)}
        ),
    )
    search_fields = ('email', 'username',)
    ordering = ('email', 'username',)
admin.site.register(CustomUser, CustomUserAdmin)