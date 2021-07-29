from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.views.generic import TemplateView
from .forms import TokenizerForm


template_name = "tokenizer.html"

class IndexView(TemplateView):
    template_name = "tokenizer.html"
    

def tokenizer_form(request):
    if request.method == 'POST':
        form = TokenizerForm(request.POST)

        if form.is_valid():
            """ 追記"""
            sent = form.cleaned_data['sentences']
            data = {
                'form': form,
                "add_index" : sent,
            }
            return render(request, template_name, data)
    else:
        form = TokenizerForm()

    return render(request, template_name, {'form': form})
    
def add_index(request):
    str_out = "you can tokenize"
    portfolio_data = {
        "add_index" : str_out,
    }
    return render(request, template_name, portfolio_data)

    
index = IndexView.as_view()
