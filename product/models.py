from django.db import models
from .category_choice import CATEGORY
# Create your models here.
class Product(models.Model):
    title = models.CharField(default='',max_length=100)
    selling_price = models.FloatField(default='',blank=True,null=True)
    discounted_price = models.FloatField(default='')
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY,blank=True,null=True)
    product_image = models.TextField(blank=True,null=True)
    def __str__(self) -> str:
        return f'{self.id}-{self.title}'