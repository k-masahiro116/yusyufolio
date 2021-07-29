from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from django.http.request import HttpRequest
from django.http import HttpResponse

# Create your views here.
from django.views.generic import TemplateView

template_name = "chat/room.html"
template_name2 = "chat/index.html"


def index(request):
    return render(request, template_name2, {})


def room(request, room_name):
    return render(request, template_name, {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
