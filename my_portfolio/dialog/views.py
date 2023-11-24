from django.urls import reverse_lazy
from .forms import PostCreateForm
from .models import Post, HDSR_Model
from django.db.models import Q
from .chains import ChitChat, StrictTask, Detector, ConcatChain, Parse
from .hdsr import HDSR
from django.contrib.auth.mixins import LoginRequiredMixin
import json

# Create your views here.
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'dialog/index.html'
    
class EvaluationView(LoginRequiredMixin, generic.ListView):
    template_name = 'dialog/evaluation.html'
    model = HDSR_Model
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        def get_index_list():
            index_list = []
            post_list = []
            for object in Post.objects.all():
                index_list.append(object.index)
                post_list.append(object)
            index_list = list(filter(None, list(set(index_list))))
            return {'index_list': index_list, 'post_list': post_list}
            
        context.update(get_index_list())
        return context
    
class EvaluationDetailView(generic.DetailView):
    template_name = 'dialog/evaluation_detail.html'
    model = Post
    chain = Parse()
    calc_model = HDSR()
    def get_context_data(self,**kwargs):
        post_list = []
        hdsr_text = ""
        hdsr_obj = None
        for post in Post.objects.all():
            if self.object.index == post.index:
                post_list.append(post)
                hdsr_text = hdsr_text+"\n{0}:{1}".format(post.speaker, post.text)
        if not HDSR_Model.objects.filter(Q(index__icontains=self.object.index)):
            self.input_HDSR_Model(hdsr_text)
        for obj in HDSR_Model.objects.all():
            if self.object.index == obj.index:
                hdsr_obj = obj
                break
        context = super().get_context_data(**kwargs)
        context.update({"post_list": post_list, "hdsr_list": json.loads(hdsr_obj.json),  "score": hdsr_obj.score})
        return context
    
    def input_HDSR_Model(self, hdsr_text):
        def parse(hdsr_text):
            text = self.chain.run(hdsr_text)
            l = text.split("\n")
            hdsr_dict = {}
            for i in l:
                hdsr_text = i.replace(" ", "")
                key, value = hdsr_text.split(":")
                hdsr_dict[key] = value
            return hdsr_dict
        hdsr_dict = parse(hdsr_text)
        slot_score = self.calc_model(hdsr_dict)
        score = sum(slot_score.values())
        hdsr_list = []
        for name, value in hdsr_dict.items():
            hdsr_list.append({"name": name, "value": value, "score": slot_score[name] })
        HDSR_Model.objects.create(json=json.dumps(hdsr_list), index=self.object.index, date=self.object.date, score=score)
    
    
class PostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        def get_last_post():
            obj = self.object_list[len(self.object_list)-1] if len(self.object_list) > 0 else Post()
            return {"last_post": "'"+obj.text.replace("\n", "")+"'", "last_text": obj.text, "last_speaker": obj.speaker, "last_date": obj.date}
            
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
    chain = ConcatChain(chitchat=ChitChat(), detector=Detector(), strict=StrictTask())
    success_url = reverse_lazy('dialog:post_list')
    model_name = ""
    last_index = 0
    def post(self, request, *args, **kwargs):
        self.last_index = self.model.objects.all().last().index
        valid = super().post(request, *args, **kwargs)
        self.eldely_care_llms()
        return valid
                
    def eldely_care_llms(self):
        form = self.get_form()
        index = 0
        response = self.chain.run(form.instance.text)
        if self.chain.pre_model == self.chain.model and self.chain.model == "strict":
            index = self.next_index()
            form.instance.index = index
            self.form_valid(form)
        self.model.objects.create(speaker="ワンコ", text=response, index=index)
        
    def next_index(self):
        object_list = self.model.objects.all()
        if self.last_index > 0:
            return self.last_index
        index_list = list(filter(None, [ obj.index for obj in object_list ]))+[0]
        return max(index_list) + 1
        

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
