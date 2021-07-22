from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel): 
    kakao_id    = models.CharField(max_length=200)
    name        = models.CharField(max_length=200, null=True)
    profile_url = models.CharField(max_length=2000, null=True)

    class Meta: 
        db_table = 'users'

class Host(TimeStampModel): 
    user        = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    nickname    = models.CharField(max_length=200)
    profile_url = models.CharField(max_length=2000)
    is_deleted  = models.BooleanField(default=False)

    class Meta: 
        db_table = 'hosts'