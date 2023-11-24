from ..hdsr.eval import Eval

class HDSR(Eval):
    slot_correct = {
        "名前": [],
        "年齢": [24, 25, 60],
        "三つの言葉の復唱": ["桜", "猫", "電車"],
        "三つの言葉の暗唱": ["桜", "猫", "電車"],
        "居場所": ["病院", "教習所", "自宅"],
        "100引く7": ["93"],
        "93引く7": ["86"],
        "年月日曜日": [],
        "3、5、2、9の逆唱": ["9253"],
        "2、8、6の逆唱": ["682"],
        "picture": ["はさみ", "ぺん", "たばこ", "くし", "とけい"],
        "知っている野菜": []
    }

    def __init__(self):
        super().__init__()
        self.slot_calc = {
            "名前": super().calc_person,
            "年齢": super().calc_age,
            "三つの言葉の復唱": super().calc_memory,
            "三つの言葉の暗唱": super().calc_memory,
            "居場所": super().calc_location,
            "100引く7": super().calc_subtraction,
            "93引く7": super().calc_subtraction,
            "年月日曜日": super().calc_now,
            "2、8、6の逆唱": super().calc_reverse,
            "3、5、2、9の逆唱": super().calc_reverse,
            "知っている野菜": super().calc_vege,
        }

    def __call__(self, slots={}):
        slot_score = {}
        getd = {}
        for slot, calc in self.slot_calc.items():
            ans = []
            if slot in slots.keys():
                ans.append(slots.get(slot, ""))
            slot_score[slot] = calc(ans, self.slot_correct.get(slot, []))
        getd["score"] = str(sum(slot_score.values()))
        
        return slot_score
