from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin personalizado para o modelo User
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'status', 'is_staff')
    list_filter = ('status', 'is_staff', 'is_superuser', 'is_active', 'groups')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Status'), {'fields': ('status', 'is_active')}),
        (_('Permissões'), {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined', 'data_criacao')}),
    )
    
    readonly_fields = ('data_criacao', 'date_joined', 'last_login')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'status', 'is_active'),
        }),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)