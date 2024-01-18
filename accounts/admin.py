from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomizeUserAdmin(UserAdmin):

    list_display = ('email', 'password', 'is_staff',)
    list_filter = ('is_staff',)
    fieldsets = (
        ('ユーザー情報', {'fields': ('email', 'password')}),
        ('権限付与',{'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    ordering = ('pk',)

    add_fieldsets = (
        ('ユーザー新規作成', {'fields': ('email', 'password1', 'password2', )}),
        ('権限付与', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
    )

    add_form = SignupForm
    inlines = (ProfileInline, )

admin.site.unregister(Group)
admin.site.register(User, CustomizeUserAdmin)
