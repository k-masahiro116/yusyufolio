from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone # django で日付を管理するためのモジュール
# Create your models here.

class HDSR_Model(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, null=True, blank=True)
    asigned = models.BooleanField(default=False, help_text='割り当てられていればTrue')
    name = models.CharField('名前', max_length=200, blank=True, null=True)
    age = models.CharField('年齢', max_length=200, blank=True, null=True)
    today = models.CharField('年月日曜日', max_length=200, blank=True, null=True)
    place = models.CharField('居場所', max_length=200, blank=True, null=True)
    repeat = models.CharField('三つの言葉の復唱', max_length=200, blank=True, null=True)
    recite = models.CharField('三つの言葉の暗唱', max_length=200, blank=True, null=True)
    backwards1 = models.CharField('2、8、6の逆唱', max_length=200, blank=True, null=True)
    backwards2 = models.CharField('3、5、2、9の逆唱', max_length=200, blank=True, null=True)
    vege = models.CharField('知っている野菜', max_length=200, blank=True, null=True)
    math1 = models.CharField('100引く7', max_length=200, blank=True, null=True)
    math2 = models.CharField('93引く7', max_length=200, blank=True, null=True)
    age_score = models.IntegerField(default=0, blank=True, null=True)
    today_score = models.IntegerField(default=0, blank=True, null=True)
    place_score = models.IntegerField(default=0, blank=True, null=True)
    repeat_score = models.IntegerField(default=0, blank=True, null=True)
    recite_score = models.IntegerField(default=0, blank=True, null=True)
    backwards1_score = models.IntegerField(default=0, blank=True, null=True)
    backwards2_score = models.IntegerField(default=0, blank=True, null=True)
    vege_score = models.IntegerField(default=0, blank=True, null=True)
    math1_score = models.IntegerField(default=0, blank=True, null=True)
    math2_score = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateTimeField('日付', default=timezone.now)
    score = models.IntegerField('スコア総和', default=-1)

    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return "ID: "+str(self.id) +",  記録日:"+self.date.strftime('%Y/%m/%d %H:%M')+",  SCORE: "+str(self.score)+"/25"
    
    def set_from_dict(self, hdsr_dict):
        self.name = hdsr_dict.get("名前", "")
        self.age = hdsr_dict.get("年齢", "")
        self.place = hdsr_dict.get("居場所", "")
        self.today = hdsr_dict.get("年月日曜日", "")
        self.repeat = hdsr_dict.get("三つの言葉の復唱", "")
        self.recite = hdsr_dict.get("三つの言葉の暗唱", "")
        self.math1 = hdsr_dict.get("100引く7", "")
        self.math2 = hdsr_dict.get("93引く7", "")
        self.backwards1 = hdsr_dict.get("2、8、6の逆唱","")
        self.backwards2 = hdsr_dict.get("3、5、2、9の逆唱","")
        self.vege = hdsr_dict.get("知っている野菜","")
        self.asigned = True
        self.save()
    
    def return_self(self):
        return {
            "名前": self.name,
            "年齢": self.age,
            "居場所": self.place,
            "年月日曜日": self.today,
            "三つの言葉の復唱": self.repeat,
            "三つの言葉の暗唱": self.recite,
            "100引く7": self.math1,
            "93引く7": self.math2,
            "2、8、6の逆唱": self.backwards1,
            "3、5、2、9の逆唱": self.backwards2,
            "知っている野菜": self.vege,
        }
    
    def set_score_from_dict(self, slot_score):
        self.age_score = slot_score.get("年齢", 0)
        self.place_score = slot_score.get("居場所", 0)
        self.today_score = slot_score.get("年月日曜日", 0)
        if self.repeat_score == 0:
            self.repeat_score = slot_score.get("三つの言葉の復唱", 0)
        if self.recite_score == 0:
            self.recite_score = slot_score.get("三つの言葉の暗唱", 0)
        if self.math1_score == 0:
            self.math1_score = slot_score.get("100引く7", 0)
        if self.math2_score == 0:
            self.math2_score = slot_score.get("93引く7", 0)
        if self.backwards1_score == 0:
            self.backwards1_score = slot_score.get("2、8、6の逆唱", 0)
        if self.backwards2_score == 0:
            self.backwards2_score = slot_score.get("3、5、2、9の逆唱", 0)
        if self.vege_score == 0:
            self.vege_score = slot_score.get("知っている野菜", 0)
        self.sum_score()
        self.save()
    def sum_score(self):
        self.score = self.age_score+self.place_score+self.today_score+self.repeat_score+self.recite_score+self.math1_score+self.math2_score+self.backwards1_score+self.backwards2_score+self.vege_score
    
class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, null=True, blank=True)
    speaker = models.CharField('話者', max_length=200)
    text = models.TextField('本文', blank=True, null=False)
    date = models.DateTimeField('日付', default=timezone.now)
    index = models.ForeignKey(
        HDSR_Model, 
        on_delete=models.CASCADE,
        verbose_name='index',
        blank=True,
        null=True,
    )

    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return self.speaker # 記事タイトルを返す
    
    
GENDER_CHOICES = [
    ('女性', '女性'),
    ('男性', '男性'),
]

class Userdata(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None, null=True, blank=True)
    name = models.CharField('名前', max_length=200)
    age = models.IntegerField('年齢', default=0)
    sex = models.CharField('性別', max_length=2, choices=GENDER_CHOICES)
    birth = models.DateField('生年月日')
    place = models.CharField('場所', max_length=200)
    max_score = models.IntegerField('最高スコア', default=0)
    min_score = models.IntegerField('最低スコア', default=0)
    hdsr = models.ManyToManyField(HDSR_Model, verbose_name="HDS-R", blank=True)
    
    def __str__(self): # Post モデルが直接呼び出された時に返す値を定義
        return self.name # 記事タイトルを返す