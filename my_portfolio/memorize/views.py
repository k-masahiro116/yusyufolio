from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models

# Create your views here.
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup
from django.utils.html import mark_safe
import re

dir = "memorize/"
filenames = {
    "test": "test.html",
    "news": "news.html",
    "diary": "diary.html",
    "corona": "corona.html",
    "youtube": "youtube.html",
    "research": "research.html",
}

def add_index(request):
    str_out = "a"
    portfolio_data = {
        "add_index" : str_out,
    }
    return render(request, dir+filenames["test"], portfolio_data)

class WebScrape:
    def scrape_livedoor_news(self, url):
        li_data = []
        href_data = []
        news_ol = []
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        soup_ol = soup.find("ol")
        for li in soup_ol.find_all("li"):
            li_data.append(mark_safe(li.get_text()))
        for href in soup_ol.find_all("a"):
            href_data.append(mark_safe(href.get("href")))
        for li, href in zip(li_data, href_data):
            news_ol.append({
                "title": li,
                "href": href,
            })
        return news_ol

    def scrape_yahoo_news(self, url):
        li_data = []
        href_data = []
        news_ul = []
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        data_list = soup.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
        for data in data_list:
            li_data.append(mark_safe(data.get_text()))
            href_data.append(mark_safe(data.attrs["href"]))
        for li, href in zip(li_data, href_data):
            news_ul.append({
                "title": li,
                "href": href,
            })
        return news_ul

    def web_scrape(self, search_word = "コロナ"):
        web_ul = []

        # 上位から何件までのサイトを抽出するか指定する
        pages_num = 10 + 1

        # print(f'【検索ワード】{search_word}')

        # Googleから検索結果ページを取得する
        url = f'https://www.google.co.jp/search?hl=ja&num={pages_num}&q={search_word}'
        request = requests.get(url)

        # Googleのページ解析を行う
        soup = BeautifulSoup(request.text, "html.parser")
        search_site_list = soup.select('div.kCrYT > a')

        # ページ解析と結果の出力
        for rank, site in zip(range(1, pages_num), search_site_list):
            try:
                site_title = site.select('h3.zBAuLc')[0].text
            except IndexError:
                site_title = site.select('img')[0]['alt']
            site_url = site['href'].replace('/url?q=', '')
            idx = site_url.find("&sa=U&ved=2")
            # 結果を出力する
            web_ul.append({
                "title" : site_title,
                "href" : site_url[:idx],
            })
            
        return web_ul

def forecast(request):
    ws = WebScrape()
    url = "http://weather.livedoor.com/forecast/webservice/json/v1?city=130010"
    livedoor = ws.scrape_livedoor_news(url)
    url = "https://news.yahoo.co.jp"
    yahoo = ws.scrape_yahoo_news(url)
    web = ws.web_scrape()
    
    news_site = {
        "livedoor" : livedoor,
        "yahoo" : yahoo,
        "web" : web,
    }
    
    return render(request, dir+filenames["news"], news_site)


def diary(request):
    return render(request, dir+filenames["diary"])

def corona(request):
    return render(request, dir+filenames["corona"])
    
def youtube(request):
    return render(request, dir+filenames["youtube"])

def research(request):
    return render(request, dir+filenames["research"])

