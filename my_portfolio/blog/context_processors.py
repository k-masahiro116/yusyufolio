from .models import Post
import requests
from bs4 import BeautifulSoup

def common(request):
    post_month_list = Post.objects.dates('date', 'month' , order='DESC')
    category_list = []
    for object in Post.objects.all():
        category_list.append(object.category)
    category_list = list(filter(None, list(set(category_list))))
    return {'category_list': category_list, 'post_month_list': post_month_list}

def common_list(request):
    all = Post.objects.order_by("-id")
    return {'newest_post_list': all}

def common_weather(request):
    context = {}
    url_forecast = 'https://tenki.jp/forecast/3/16/4410/13208/'
    fdict = scrape_weather(url_forecast)
    forecast = fdict["today"]["forecasts"][0]
    context["weather"] = "天気: "+forecast["weather"]
    context["temp_high"] = "最高気温: "+forecast["high_temp"]
    context["temp_low"] = "最低気温: "+forecast["low_temp"]
    context["rain_probability"] = "降水確率: "
    context["rain_probability_0006"] = "00-06: "+forecast["rain_probability"]['00-06'] 
    context["rain_probability_0612"] = "06-12: "+ forecast["rain_probability"]['06-12']
    context["rain_probability_1218"] = "12-18: "+ forecast["rain_probability"]['12-18']
    context["rain_probability_1824"] = "18-24: "+ forecast["rain_probability"]['18-24']
    return context

def scrape_weather(url):
    s = soup(url)
    dict = {}
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
    data["forecasts"] = []
    # ## 取得
    weather           = soup.select('.weather-telop')[0]
    high_temp         = soup.select("[class='high-temp temp']")[0]
    high_temp_diff    = soup.select("[class='high-temp tempdiff']")[0]
    low_temp          = soup.select("[class='low-temp temp']")[0]
    low_temp_diff     = soup.select("[class='low-temp tempdiff']")[0]
    rain_probability  = soup.select('.rain-probability > td')
    wind_wave         = soup.select('.wind-wave > td')[0]

    # ## 格納
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
    return data