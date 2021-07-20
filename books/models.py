from django.db       import models

from core.models     import TimeStampModel
from products.models import Product
from users.models    import User

class Book(TimeStampModel): 
    user       = models.ForeignKey('User', on_delete=models.CASCADE)
    product    = models.ForeignKey('Product', on_delete=models.CASCADE)
    status     = models.ForeignKey('BookStatus', on_delete=models.CASCADE)
    price      = models.DecimalField(decimal_places=2, max_digits=10)
    start_date = models.DateTimeField(null=True)
    end_date   = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta: 
        db_table = 'books'

class BookStatus(TimeStampModel):
    status = models.CharField(max_length=200)

    class Meta: 
        db_table='bookstatus'