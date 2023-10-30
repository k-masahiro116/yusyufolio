from django.db import models
from django.utils import timezone # django で日付を管理するためのモジュール
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField('タイトル', max_length=200)
    category = models.CharField('カテゴリ', max_length=200, null = True)
    text = models.TextField('本文')
    date = models.DateTimeField('日付', default=timezone.now)
    redate = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return self.title # 記事タイトルを返す
    
    