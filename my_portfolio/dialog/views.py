from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import QueryDict
from .forms import PostCreateForm
from .models import Post 
from django.db.models import Q
from typing import Any, Dict, Union
from .chains import ChitChat, StrictTask, Detector, ConcatChain
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'dialog/index.html'
    
class PostListView(LoginRequiredMixin, generic.ListView): # generic の ListViewクラスを継承
    model = Post # 一覧表示させたいモデルを呼び出し
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        url_forecast = 'https://tenki.jp/forecast/3/16/4410/13208/'
        fdict = main(url_forecast)
        forecast = fdict["today"]["forecasts"][0]
        context["weather"] = "天気: "+forecast["weather"]
        context["temp_high"] = "最高気温: "+forecast["high_temp"]
        context["temp_low"] = "最低気温: "+forecast["low_temp"]
        context["rain_probability"] = "降水確率: "
        context["rain_probability_0006"] = "00-06: "+forecast["rain_probability"]['00-06'] 
        context["rain_probability_0612"] = "06-12: "+ forecast["rain_probability"]['06-12']
        context["rain_probability_1218"] = "12-18: "+ forecast["rain_probability"]['12-18']
        context["rain_probability_1824"] = "18-24: "+ forecast["rain_probability"]['18-24']
        def get_last_post():
            obj = self.object_list[len(self.object_list)-1] if len(self.object_list) > 0 else Post()
            return {"last_post": "'"+obj.text+"'", "last_text": obj.text, "last_speaker": obj.speaker, "last_date": obj.date}
            
        context.update(get_last_post())
        return context

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = Post.objects.filter(
                Q(speaker__icontains=q_word) | Q(text__icontains=q_word) | Q(date__icontains=q_word))
        else:
            object_list = Post.objects.all()
        return object_list
    
class PostCreateView(generic.CreateView): # 追加
    model = Post # 作成したい model を指定
    form_class = PostCreateForm # 作成した form クラスを指定
    chitchat = ConcatChain(wanco=ChitChat(), detector=Detector(), strict=StrictTask())
    success_url = reverse_lazy('dialog:post_list')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        valid = super().post(request, *args, **kwargs)
        self.repost()
        return valid
    
    def repost(self):
        form = self.get_form()
        if form.is_valid():
            form_kwargs = self.get_form_kwargs()
            input_text = form_kwargs.get("data").get("text")
            response = self.eldely_care_llms(input_text = input_text)
            form_kwargs["data"] = QueryDict('speaker={}&text={}'.format("ワンコ", response))
            object = self.model()
            object.speaker = "AI"
            form_kwargs["instance"] = object
            form = self.get_form(form_kwargs=form_kwargs)
            if form.is_valid():
                self.form_valid(form)
            else:
                self.form_invalid(form)
                
    def eldely_care_llms(self, input_text=""):
        return self.chitchat.run({"text": input_text, "volume": 65})
        
    def get_form(self, form_class=None, form_kwargs=None):
        """Return an instance of the form to be used in this view."""
        if form_kwargs is not None:
            if form_class is None:
                form_class = self.get_form_class()
            return form_class(**form_kwargs)
        return super().get_form(form_class=form_class)

    

class PostDetailView(generic.DetailView): # 追加
    model = Post  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む
    
class PostUpdateView(generic.UpdateView): # 追加
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    success_url = reverse_lazy('dialog:post_list')
    
class PostDeleteView(generic.DeleteView): # 追加
    model = Post
    success_url = reverse_lazy('dialog:post_list')
    
    
import re
import requests
from bs4 import BeautifulSoup
import json
#----------------------------------------
#copyed by https://kinformation.sakura.ne.jp/20170715-01
#----------------------------------------

def main(url):
    # bs4でパース
    s = soup(url)

    dict = {}

    # 予測地点
    l_pattern = r"(.+)の今日明日の天気"
    l_src = s.title.text
    dict['location'] = re.findall(l_pattern, l_src)[0]
    # print(dict['location'] + "の天気")

    soup_tdy = s.select('.today-weather')[0]
    soup_tmr = s.select('.tomorrow-weather')[0]

    dict["today"] = forecast2dict(soup_tdy)
    dict["tomorrow"] = forecast2dict(soup_tmr)

    # JSON形式で出力
    # print(json.dumps(dict, ensure_ascii=False))
    return dict

def soup(url):
    r = requests.get(url)
    html = r.text.encode(r.encoding)
    return BeautifulSoup(html, 'lxml')

def forecast2dict(soup):
    data = {}

    # 日付処理
    d_pattern = r"(\d+)月(\d+)日\(([土日月火水木金])+\)"
    d_src = soup.select('.left-style')
    date = re.findall(d_pattern, d_src[0].text)[0]
    data["date"] = "%s-%s(%s)" % (date[0], date[1], date[2])
    # print("=====" + data["date"] + "=====")

    # ## 取得
    weather           = soup.select('.weather-telop')[0]
    high_temp         = soup.select("[class='high-temp temp']")[0]
    high_temp_diff    = soup.select("[class='high-temp tempdiff']")[0]
    low_temp          = soup.select("[class='low-temp temp']")[0]
    low_temp_diff     = soup.select("[class='low-temp tempdiff']")[0]
    rain_probability  = soup.select('.rain-probability > td')
    wind_wave         = soup.select('.wind-wave > td')[0]

    # ## 格納
    data["forecasts"] = []
    forecast = {}
    forecast["weather"] = weather.text.strip()
    forecast["high_temp"] = high_temp.text.strip()
    forecast["high_temp_diff"] = high_temp_diff.text.strip()
    forecast["low_temp"] = low_temp.text.strip()
    forecast["low_temp_diff"] = low_temp_diff.text.strip()
    every_6h = {}
    for i in range(4):
        time_from = 0+6*i
        time_to   = 6+6*i
        itr       = '{:02}-{:02}'.format(time_from,time_to)
        every_6h[itr] = rain_probability[i].text.strip()
    forecast["rain_probability"] = every_6h
    forecast["wind_wave"] = wind_wave.text.strip()

    data["forecasts"].append(forecast)

    # print(
    #     "天気              ： " + forecast["weather"] + "\n"
    #     "最高気温(C)       ： " + forecast["high_temp"] + "\n"
    #     "最高気温差(C)     ： " + forecast["high_temp_diff"] + "\n"
    #     "最低気温(C)       ： " + forecast["low_temp"] + "\n"
    #     "最低気温差(C)     ： " + forecast["low_temp_diff"] + "\n"
    #     "降水確率[00-06]   ： " + forecast["rain_probability"]['00-06'] + "\n"
    #     "降水確率[06-12]   ： " + forecast["rain_probability"]['06-12'] + "\n"
    #     "降水確率[12-18]   ： " + forecast["rain_probability"]['12-18'] + "\n"
    #     "降水確率[18-24]   ： " + forecast["rain_probability"]['18-24'] + "\n"
    #     "風向              ： " + forecast["wind_wave"] + "\n"
    # )

    return data

if __name__ == '__main__':
    # 世田谷区の一時間ごとの気象情報URL
    # URL = 'https://tenki.jp/forecast/3/16/4410/13112/1hour.html'
    URL = 'https://tenki.jp/forecast/3/16/4410/13208/'
    main(URL)
