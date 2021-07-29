
from django import forms


class TokenizerForm(forms.Form):
    sentences = forms.CharField(label='Sentences', widget=forms.Textarea)