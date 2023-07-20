from rest_framework import serializers
from .models import Cart
from drf_yasg.utils import swagger_auto_schema
class CartSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')
    product_price = serializers.FloatField(source='product.discounted_price')
    product_img = serializers.CharField(source = 'product.product_image')
    class Meta:
        model = Cart
        fields = '__all__'
class CartPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("product",)
    