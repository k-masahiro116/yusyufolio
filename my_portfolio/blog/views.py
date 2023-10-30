from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import PostCreateForm
from .models import Post 
from django.db.models import Q

# Create your views here.
from django.views import generic
from django.shortcuts import redirect

class IndexView(generic.TemplateView):
    template_name = 'blog/index.html'
    
def redirect_view(request):
    models = Post.objects.all()
    model = models.last()
    if len(models) > 0:
        url = "post_detail/{}".format(model.pk)
        return redirect(url)
    else:
        return redirect("post_list")
    
class PostSidebarView(generic.ListView): # generic の ListViewクラスを継承
    model = Post # 一覧表示させたいモデルを呼び出し
    
class PostListView(generic.ListView): # generic の ListViewクラスを継承
    model = Post # 一覧表示させたいモデルを呼び出し
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # url_forecast = 'https://tenki.jp/forecast/3/16/4410/13208/'
        # fdict = main(url_forecast)
        # forecast = fdict["today"]["forecasts"][0]
        # context["weather"] = "天気: "+forecast["weather"]
        # context["temp_high"] = "最高気温: "+forecast["high_temp"]
        # context["temp_low"] = "最低気温: "+forecast["low_temp"]
        # context["rain_probability"] = "降水確率: "
        # context["rain_probability_0006"] = "00-06: "+forecast["rain_probability"]['00-06'] 
        # context["rain_probability_0612"] = "06-12: "+ forecast["rain_probability"]['06-12']
        # context["rain_probability_1218"] = "12-18: "+ forecast["rain_probability"]['12-18']
        # context["rain_probability_1824"] = "18-24: "+ forecast["rain_probability"]['18-24']
        context.update(get_common_data())
        return context

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word:
            object_list = Post.objects.filter(
                Q(title__icontains=q_word) | Q(text__icontains=q_word) | Q(date__icontains=q_word) | Q(category__icontains=q_word))
        else:
            object_list = Post.objects.all()
        return object_list
    
class PostCreateView(generic.CreateView): # 追加
    model = Post # 作成したい model を指定
    form_class = PostCreateForm # 作成した form クラスを指定
    success_url = reverse_lazy('blog:post_list') # 記事作成に成功した時のリダイレクト先を指定
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # url_forecast = 'https://tenki.jp/forecast/3/16/4410/13208/'
        # fdict = main(url_forecast)
        # forecast = fdict["today"]["forecasts"][0]
        # context["weather"] = "天気: "+forecast["weather"]
        # context["temp_high"] = "最高気温: "+forecast["high_temp"]
        # context["temp_low"] = "最低気温: "+forecast["low_temp"]
        # context["rain_probability"] = "降水確率: "
        # context["rain_probability_0006"] = "00-06: "+forecast["rain_probability"]['00-06'] 
        # context["rain_probability_0612"] = "06-12: "+ forecast["rain_probability"]['06-12']
        # context["rain_probability_1218"] = "12-18: "+ forecast["rain_probability"]['12-18']
        # context["rain_probability_1824"] = "18-24: "+ forecast["rain_probability"]['18-24']
        form = self.get_form()
        print(form.fields["text"].help_text)
        return context

class PostDetailView(generic.DetailView): # 追加
    model = Post  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        objects = Post.objects.order_by()
        
        index = list(objects).index(object)
        if len(objects) > index+1:
            obj = list(objects)[index+1]
            context["next_pk"] = obj.pk
        else:
            context["next_pk"] = object.pk
        if index-1 >= 0:
            obj = list(objects)[index-1]
            context["pre_pk"] = obj.pk
        else:
            context["pre_pk"] = object.pk
        context.update(get_common_data())
        return context
        
    
class PostUpdateView(generic.UpdateView): # 追加
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    success_url = reverse_lazy('blog:post_list')
    
class PostDeleteView(generic.DeleteView): # 追加
    model = Post
    success_url = reverse_lazy('blog:post_list')
    
    
def get_common_data():
    #サイドバーの月別投稿ー一覧
    post_month_list = Post.objects.dates('date', 'month' , order='DESC')
    category_list = []
    for object in Post.objects.all():
        category_list.append(object.category)
    category_list = list(filter(None, list(set(category_list))))
    return {'category_list': category_list, 'post_month_list': post_month_list}
    
import re
import requests
from bs4 import BeautifulSoup

def main(url):
    # bs4でパース
    s = soup(url)
    dict = {}
    # 予測地点
    l_pattern = r"(.+)の今日明日の天気"
    l_src = s.title.text
    dict['location'] = re.findall(l_pattern, l_src)[0]

    soup_tdy = s.select('.today-weather')[0]
    soup_tmr = s.select('.tomorrow-weather')[0]
    dict["today"] = forecast2dict(soup_tdy)
    dict["tomorrow"] = forecast2dict(soup_tmr)
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
