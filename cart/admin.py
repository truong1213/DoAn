from django.contrib import admin
from .models import Cart
# Register your models here.
@admin.register(Cart)
class Cart(admin.ModelAdmin):
    pass