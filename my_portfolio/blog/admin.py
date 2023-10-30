from django import forms
from django.contrib import admin
from .models import * # 追加
from django_summernote.admin import SummernoteModelAdmin

class PostCreateForm(forms.ModelForm): # DjangoのModelFormでは強力なValidationを使える
    summernote_fields = ('text')
    class Meta:
        model = Post # Post モデルと接続し、Post モデルの内容に応じてformを作ってくれる
        fields = ('title', 'text') # 入力するカラムを指定
admin.site.register(Post, SummernoteModelAdmin)

