from .models import CustomUser,TokenRegister,TokenResetPassword
from rest_framework import serializers
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email","username","password","name","sex","phone","address")
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
class TokenRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenRegister
        fields  = '__all__'
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("name","sex","phone","address")
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("password",)
class TokenResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenResetPassword
        fields  = '__all__'
