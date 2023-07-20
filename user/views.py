from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView,CreateAPIView
from auth_user.models import CustomUser
from auth_user.serializers import ProfileSerializer
from rest_framework.response import Response
# Create your views here.
class Profile(RetrieveAPIView,CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username,
            'phone': user.phone,
            'sex': user.sex,
            'address':user.address,
            'name': user.name,
        })
    def post(self, request, *args, **kwargs):
        data = request.data
        user = CustomUser.objects.filter(email=request.user).first()
        user.name = data['name']
        user.phone = data['phone']
        user.sex = data['sex']
        user.address = data['address']
        user.save()
        return Response({
            'email': user.email,
            'username': user.username,
            'phone': user.phone,
            'sex': user.sex,
            'address':user.address,
            'name': user.name,
        })