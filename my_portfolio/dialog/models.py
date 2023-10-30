from django.db import models
from django.utils import timezone # django で日付を管理するためのモジュール

# Create your models here.

class Post(models.Model):
    speaker = models.CharField('話者', max_length=200)
    text = models.TextField('本文')
    date = models.DateTimeField('日付', default=timezone.now)

    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return self.speaker # 記事タイトルを返す
    
    