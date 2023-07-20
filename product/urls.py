from django.urls import path
from . import views
urlpatterns = [
    path('dien-thoai/',views.MobilePhone.as_view(),name="mobilephone"),
    path('laptop/',views.Laptop.as_view(),name="laptop"),
    path('tablet/',views.Tablet.as_view(),name="tablet"),
    path('phu-kien/',views.Accessories.as_view(),name="accessories"),
    path('search/',views.Search.as_view(),name="searchProduct"),
    path('sort-by-price-ascending/',views.SortByPriceAscending.as_view(),name='SortByPriceAscending'),
    path('detail/<pk>/',views.ProductDetail.as_view(),name='productdetail'),
    path('add/',views.ProductAdd.as_view(),name="productadd"),
    path('seed-data/',views.SeedData.as_view(),name='seeddata'),
    
]