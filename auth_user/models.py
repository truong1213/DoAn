from django.db import models
from django.contrib.auth.models import AbstractUser
from .sexchoice import SEX_CHOICE
import uuid
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICE,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    name = models.CharField(blank=True,null=True,max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
class TokenRegister(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    email = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="tokenregister")
    create_at = models.DateTimeField(auto_now_add=True)
class TokenResetPassword(models.Model):
    token = models.UUIDField(default=uuid.uuid4)
    email = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="tokenresetpassword")
    create_at = models.DateTimeField(auto_now_add=True)
    