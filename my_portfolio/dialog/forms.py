from django import forms
from .models import Post, HDSR_Model

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('speaker', 'text')
        
class EvalCreateForm(forms.ModelForm): 
    class Meta:
        model = HDSR_Model
        fields = ('json',) 