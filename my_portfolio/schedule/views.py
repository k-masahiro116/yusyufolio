from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
import plotly.graph_objects as go
import numpy as np

def index(request):
    return render(request, "schedule.html", {})

class IndexView(TemplateView):
    template_name = "schedule.html"
    
draw = IndexView.as_view()

