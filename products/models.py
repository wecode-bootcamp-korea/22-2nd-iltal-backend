from django.db   import models

from users.models import Host
from core.models import TimeStampModel

class Category(TimeStampModel): 
    name = models.CharField(max_length=200)

    class Meta: 
        db_table = 'categories'

class Subcategory(TimeStampModel): 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')
    name     = models.CharField(max_length=200)

    class Meta: 
        db_table = 'subcategories'

class Product(TimeStampModel):
    subcategory    = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')
    host           = models.ForeignKey(Host, on_delete=models.CASCADE)
    title          = models.CharField(max_length=200)
    coordinate     = models.JSONField()
    region         = models.CharField(max_length=200)
    price          = models.DecimalField(decimal_places=2, max_digits=10)
    is_group       = models.BooleanField()
    backgruond_url = models.CharField(max_length=2000)
    is_deleted     = models.BooleanField(default=False)

    class Meta: 
        db_table = 'products'


