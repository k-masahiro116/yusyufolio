from django.contrib import admin
from django import forms
from .models import *
from django.utils import timezone # django で日付を管理するためのモジュール

# Register your models here.
class UserdataCreateForm(forms.ModelForm): 
    class Meta:
        model = Userdata
        fields = ('name', 'age', 'sex', 'birth', 'place') 
admin.site.register(Userdata)