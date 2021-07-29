from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

# Create your views here.
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from .forms import ContactForm
template_name = "function/contact.html"




def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            """ 追記"""
            subject = form.cleaned_data['subject']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']+"\nfrom: "+sender
            myself = form.cleaned_data['myself']
            recipients = [settings.EMAIL_HOST_USER]

            if myself:
                recipients.append(sender)
            try:
                send_mail(subject, message, sender, recipients)
            except BadHeaderError:
                return HttpResponse('無効なヘッダーが見つかりました。')
            return redirect('function:complete')

    else:
        form = ContactForm()

    return render(request, template_name, {'form': form})

def complete(request):
    return render(request, 'function/complete.html')

class ContactView(TemplateView):
    template_name = "function/contact.html"
    
contact = ContactView.as_view()