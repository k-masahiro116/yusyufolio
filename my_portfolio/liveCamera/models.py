from django.db import models
from django.utils import timezone 

# Create your models here.

class UploadImage(models.Model):
    date = models.DateTimeField('日付', default=timezone.now)
    image = models.ImageField(upload_to='')

    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return self.image.name