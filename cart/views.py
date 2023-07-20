from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from product.models import Product
from .serializers import CartSerializer,CartPostSerializer
from drf_yasg.utils import swagger_auto_schema

class CartView(ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    @swagger_auto_schema(request_body=CartPostSerializer)
    def post(self, request,*args, **kwargs):
        user = request.user
        user_id = user.id
        product_id = request.data['product']
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.filter(user=user_id,product=product).first()
        if cart:
            cart.quantity +=1
            cart.save()
        else:   
            Cart.objects.create(user=user,product=product)
        return super().post(request, *args, **kwargs)
