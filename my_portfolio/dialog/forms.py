from django import forms
from .models import *

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('speaker', 'text', 'user')
        
class EvalCreateForm(forms.ModelForm): 
    class Meta:
        model = HDSR_Model
        fields = ('name','today','age','place','score', 'repeat', 'recite', 'math1', 'math2', 'backwards1', 'backwards2', 'vege'
                ,'today_score','age_score','place_score','score', 'repeat_score', 'recite_score', 'math1_score', 'math2_score', 'backwards1_score', 'backwards2_score', 'vege_score') 

class DateInput(forms.DateInput):
    input_type = 'date'
        
class UserdataCreateForm(forms.ModelForm): 
    hdsr = forms.ModelMultipleChoiceField(
        # queryset=HDSR_Model.objects.filter(userdata=None),  
        queryset=HDSR_Model.objects.all(),  
        widget=forms.CheckboxSelectMultiple,
        required=False,
        error_messages={'invalid_choice':'このHDS-R項目は存在しません'}
        )
    class Meta:
        model = Userdata
        fields = ('name', 'sex', 'birth', 'place', 'hdsr') 
        widgets = {
                'birth': DateInput(),
            }