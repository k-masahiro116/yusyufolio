from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models

# Create your views here.
from django.views.generic import TemplateView


template_name = "index.html"

class IndexView(TemplateView):
    template_name = "index.html"

    
def add_index(request):
    str_out = "a"
    portfolio_data = {
        "add_index" : str_out,
    }
    return render(request, template_name, portfolio_data)

    
index = IndexView.as_view()
