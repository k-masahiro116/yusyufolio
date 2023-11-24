import re
import datetime
import pandas as pd
import re
import MeCab
from pykakasi import kakasi  # pip3 install pykakasi　漢字とカタカナをひらがなに

kks = kakasi()
wakati = MeCab.Tagger("-Owakati")

def convf(name):
    hira = ""
    for kks_dict in kks.convert(name.strip()):
        hira = hira + kks_dict["hira"]
    return hira

def target_in_list(t, l):
    if convf(t) in l or t in l:
        return True
    return False


def ymdd_now():
    ymdd = ["year", "month", "date", "day"]
    weekd = {0: "月", 1: "火", 2: "水", 3: "木", 4: "金", 5: "土", 6: "日"}
    today = re.split("-", str(datetime.date.today()))
    today.append(datetime.date(int(today[0]), int(today[1]), int(today[2])).weekday())
    today[3] = "{}曜日".format(weekd[today[3]])
    today[0] = str(int(today[0]))+"年"
    today[1] = str(int(today[1]))+"月"
    today[2] = str(int(today[2]))+"日"
    return "".join(today)


class Eval():
    slot_score: dict = {}
    slot_calc: dict = {}
    slots: list = []

    def __init__(self):
        self.slot_score = {}
        self.slot_calc = {}
        self.slots = []

    def install_data(self, json_data):
        for slot, ans in json_data.items():
            if ans is not None:
                self.slots.append({"slot": slot, "ans": ans})

    def calc_person(self, input_data, correct=[]):
        self.person = ""
        if not type(input_data) != str:
            if input_data is not []:
                for i in input_data:
                    if type(i) is str:
                        self.person += i
                        return 1
        elif input_data != "":
            self.person = input_data
            return 1
        return 0

    def calc_age(self, data_list, correct=[75]):
        for data in data_list:
            if data == "":
                continue
            data = re.match(".*\\d", data).group()
            if any([int(data) in correct, int(data)+1 in correct, int(data)+2 in correct, int(data)-1 in correct, int(data)-2 in correct]):
                return 1
        return 0

    def calc_memory(self, data_list, correct=["さくら", "ねこ", "でんしゃ", "桜", "猫", "電車"]):
        score = 0
        for data in data_list:
            if target_in_list(data, correct):
                score = score + 1
            for i in wakati.parse(data).split():
                if target_in_list(i, correct):
                    score = score + 1
        return score

    def calc_location(self, data_list, correct=["家", "お家", "病院", "施設", "老人ホーム", "教習所", "自宅"]):
        score = 0
        for data in data_list:
            if target_in_list(data, correct):
                score = score + 2
                break
        return score

    def calc_picture(self, data_list, correct=[]):
        score = 0
        for data in data_list:
            if target_in_list(data, correct):
                score = score + 1
        return score

    def calc_subtraction(self, data_list, correct=[93]):
        score = 0
        for data in data_list:
            if data in correct:
                score = score + 1
        return score

    def calc_now(self, input_data, correct=[]):
        ymdd = ymdd_now()
        if input_data == ymdd:
            return 1
        return 0
    
    def calc_year(self, data_list, correct=[]):
        ymdd = ymdd_now()
        for data in data_list:
            if ymdd["year"] in data:
                return 1
        return 0

    def calc_month(self, data_list, correct=[]):
        ymdd = ymdd_now()
        for data in data_list:
            if ymdd["month"] in data:
                return 1
        return 0

    def calc_date(self, data_list, correct=[]):
        ymdd = ymdd_now()
        for data in data_list:
            if ymdd["date"] in data:
                return 1
        return 0

    def calc_day(self, data_list, correct=[]):
        ymdd = ymdd_now()
        for data in data_list:
            if ymdd["day"] in data:
                return 1
        return 0

    def calc_reverse(self, data_list, correct=[9253]):
        score = 0
        for data in data_list:
            if data in correct:
                score = score + 1
        return score

    def calc_vege(self, data_list, correct=[]):
        df = pd.read_csv('dialog/assets/csv/vegetables.csv')
        veges = 0
        for data in data_list:
            if target_in_list(data, df["vegetable"].values.tolist()):
                veges = veges + 1
            for i in wakati.parse(data).split():
                if target_in_list(i, df["vegetable"].values.tolist()):
                    veges = veges + 1
        if veges <= 5:
            score = 0
        elif veges == 6:
            score = 1
        elif veges == 7:
            score = 2
        elif veges == 8:
            score = 3
        elif veges == 9:
            score = 4
        else:
            score = 5
        return score
