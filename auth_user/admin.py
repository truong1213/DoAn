from django.contrib import admin
from .form import CustomUserChangeForm,CustomUserCreationForm
from .models import CustomUser,TokenRegister,TokenResetPassword
# Register your models here.
@admin.register(CustomUser)
class NewUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'is_active',
    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
    ("Thong tin co ban", {'fields': ('username', 'email', 'password', "phone", "sex","address","name")}),
    ('Phan quyen', {'fields': ('is_staff', 'is_active',
    'is_superuser', 'groups', 'user_permissions')}),
    ('Ngay thang', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
    ("Thong tin", {
    'classes': ('wide',),
    'fields': ('username', 'email', 'password1', "phone", "sex", 'password2', 'is_staff', 'is_active')}
    ),
    )
    search_fields = ('email',)
    ordering = ('email',)
@admin.register(TokenRegister)
class TokenRegister(admin.ModelAdmin):
    pass
@admin.register(TokenResetPassword)
class TokenResetPassword(admin.ModelAdmin):
    pass
