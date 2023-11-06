# project/contact/forms.py

from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(label='件名', max_length=100)
    sender = forms.EmailField(label='Email')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)
    myself = forms.BooleanField(label='', required=False)