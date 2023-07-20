from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView,CreateAPIView
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAdminUser

# Create your views here.
class MobilePhone(ListAPIView):
    queryset = Product.objects.filter(category__icontains='Điện thoại').all()
    serializer_class = ProductSerializer
class Laptop(ListAPIView):
    queryset = Product.objects.filter(category__icontains='Laptop').all()
    serializer_class = ProductSerializer
class Accessories(ListAPIView):
    queryset = Product.objects.filter(category__icontains='Phụ kiện').all()
    serializer_class = ProductSerializer
class Tablet(ListAPIView):
    queryset = Product.objects.filter(category__icontains='Tablet').all()
    serializer_class = ProductSerializer
class Search(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('keyword', openapi.IN_QUERY, description='Keyword for search', type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response('Successful Response', schema=ProductSerializer(many=True)),
        }
        )
    def get(self, request):
        search_query = request.query_params.get('keyword', '')
        print(search_query)
        products = Product.objects.filter(title__icontains=search_query)
        print(products)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({"data":serializer.data},safe= False)
class SortByPriceAscending(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering = ['price']
class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductAdd(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class SeedData(APIView):
    def get(self, request, *args, **kwargs):
        print('test')
        products = []
        for i in range(20):
            products.append(Product(
               title = f"Laptop {i}",
               selling_price = 500000+i*1000,
               discounted_price = 500000,
               description = f"description {i}",
               category = "Laptop",
               product_image ="link ảnh trên drive"
           )) 
        Product.objects.bulk_create(products)
        return JsonResponse({"message":"success"})