from django import forms
from django.contrib import admin
from .models import * # 追加
from django_summernote.admin import SummernoteModelAdmin

class PostCreateForm(forms.ModelForm): 
    summernote_fields = ('text')
    class Meta:
        model = Post 
        fields = ('title', 'text') 
admin.site.register(Post, SummernoteModelAdmin)

