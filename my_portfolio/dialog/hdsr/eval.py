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
    if t != None and (convf(t) in l  or  t in l ):
        return True
    return False

class Eval():
    def calc_age(self, input_data, correct=[75]):
        age = input_data
        age = int(re.match(".*\\d", age).group())
        if any([age in correct, age+1 in correct, age+2 in correct, age-1 in correct, age-2 in correct]):
            return 1
        return 0

    def calc_memory(self, input_data, correct=["さくら", "ねこ", "でんしゃ", "桜", "猫", "電車"]):
        score = 0
        if input_data != None:
            for i in wakati.parse(input_data).split():
                if target_in_list(i, correct):
                    score = score + 1
        return score

    def calc_memory2(self, input_data, correct=["さくら", "ねこ", "でんしゃ", "桜", "猫", "電車"]):
        score = 0
        if input_data != None:
            for i in wakati.parse(input_data).split():
                if target_in_list(i, correct):
                    score = score + 2
        return score
    
    def calc_location(self, input_data, correct=["家", "お家", "病院", "施設", "老人ホーム", "教習所", "自宅"]):
        score = 0
        if target_in_list(input_data, correct):
            score = score + 2
        return score

    def calc_subtraction(self, input_data, correct=[93]):
        score = 0
        if input_data in correct:
            score = score + 1
        return score

    def calc_now(self, input_data, correct=[]):
        ymdd = correct
        score = 0
        print(input_data, correct)
        for k in ymdd:
            if k in input_data:
                score = score + 1
        return score

    def calc_reverse(self, input_data, correct=[9253]):
        score = 0
        if input_data in correct:
            score = score + 1
        return score

    def calc_vege(self, input_data, correct=[]):
        df = pd.read_csv('dialog/assets/csv/vegetables.csv')
        veges = 0
        for i in wakati.parse(input_data).split():
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
