from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'staff_id_number', 'phone_number', 'role']
    fieldsets = (
        (None, {'fields': ['username']}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'staff_id_number', 'role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
        (
            'Personal Info', {
                'fields': ('email', 'first_name', 'last_name', 'phone_number', 'staff_id_number', 'role')
            }
        )
    )



admin.site.register(CustomUser, CustomUserAdmin)