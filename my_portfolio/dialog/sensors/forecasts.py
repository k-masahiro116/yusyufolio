import requests
import re
from datetime import datetime

#今日の天気のみ。次の日の天気などもいるか？
class Forecasts:
    city_code = "130010" # 東京都のcityコード
    url = "https://weather.tsukumijima.net/api/forecast/city/" + city_code
    def __init__(self, url=url):
        try:
            response = requests.get(url)
            response.raise_for_status()     # ステータスコード200番台以外は例外とする
        except requests.exceptions.RequestException as e:
            print("Error:{}".format(e))

        else:
            self.weather_json = response.json()
            
    @property
    def description(self):
        return self.weather_json['description']
    @property
    def description_head(self):
        return self.weather_json['description']['headlineText']
    @property
    def description_body(self):
        return self.weather_json['description']['bodyText']
    @property
    def chanceOfRain(self):
        return self.weather_json['forecasts'][0]['chanceOfRain']
    @property
    def temperature(self):
        return self.weather_json['forecasts'][0]['temperature']
    @property
    def detail(self):
        return self.weather_json['forecasts'][0]['detail']
    @property
    def weather(self):
        return self.weather_json['forecasts'][0]['detail']['weather']
    @property
    def wind(self):
        return self.weather_json['forecasts'][0]['detail']['wind']
    @property
    def wave(self):
        return self.weather_json['forecasts'][0]['detail']['wave']

if __name__ == "__main__":
    forecasts = Forecasts()
    print(forecasts.description_head)
    print(forecasts.description_body)
    print(forecasts.chanceOfRain)
    print(forecasts.temperature)
    print(forecasts.weather)