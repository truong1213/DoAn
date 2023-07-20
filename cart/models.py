from django.db import models
from auth_user.models import CustomUser
from product.models import Product
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self) -> str:
        return f'{self.user}'
