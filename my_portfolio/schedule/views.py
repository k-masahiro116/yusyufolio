import json
from .models import Event
from .forms import EventForm
from .forms import CalendarForm
from django.http import Http404
import time
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.views.generic import TemplateView
import plotly.graph_objects as go
import numpy as np
from django.middleware.csrf import get_token
from django.shortcuts import render
# def index(request):
#     return render(request, "schedule.html", {})

class IndexView(TemplateView):
    template_name = "schedule.html"
    
def index(request):
    if request.user.is_superuser:
        portfolio_data = {
            "is_superuser" : "true",
        }
    else:
        portfolio_data = {
            "is_superuser" : "false",
        }
    template = loader.get_template("schedule/index.html")
    return render(request, "schedule/index.html", portfolio_data)
    
def add_event(request):
    if request.method == "GET":
        # GETは対応しない
        raise Http404()
    # JSONの解析
    datas = json.loads(request.body)
    # バリデーション
    eventForm = EventForm(datas)
    if eventForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()
    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]
    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))
    # 登録処理
    event = Event(
        event_name=str(event_name),
        start_date=formatted_start_date,
        end_date=formatted_end_date,
    )
    event.save()
    # 空を返却
    return HttpResponse("")

def remove_event(request):
    if request.method == "GET":
        raise Http404()
    datas = json.loads(request.body)
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]
    events = Event.objects.filter(
        start_date__lt=end_date, end_date__gt=start_date, 
    )
    for event in events:
        if event.event_name == event_name:
            event.delete()
            break
    return HttpResponse("")

def edit_event(request):
    if request.method == "GET":
        raise Http404()
    datas = json.loads(request.body)
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]
    new_event_name = datas["new_event_name"]
    events = Event.objects.filter(
        start_date__lt=end_date, end_date__gt=start_date, 
    )
    for event in events:
        if event.event_name == event_name:
            event.delete()
            break
    event = Event(
        event_name=str(new_event_name),
        start_date=start_date,
        end_date=end_date,
    )
    event.save()
    return HttpResponse("")

def get_events(request):
    """
    イベントの取得
    """
    if request.method == "GET":
        # GETは対応しない
        raise Http404()
    # JSONの解析
    datas = json.loads(request.body)
    # バリデーション
    calendarForm = CalendarForm(datas)
    if calendarForm.is_valid() == False:
        # バリデーションエラー
        raise Http404()
    # リクエストの取得
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    # 日付に変換。JavaScriptのタイムスタンプはミリ秒なので秒に変換
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))
    # FullCalendarの表示範囲のみ表示
    events = Event.objects.filter(
        start_date__lt=formatted_end_date, end_date__gt=formatted_start_date
    )
    # fullcalendarのため配列で返却
    list = []
    for event in events:
        list.append(
            {
                "title": event.event_name,
                "start": event.start_date,
                "end": event.end_date,
            }
        )
    return JsonResponse(list, safe=False)

