from ..hdsr.eval import Eval
# from eval import Eval #test用

class HDSR(Eval):
    slot_correct = {
        "年齢": [],
        "三つの言葉の復唱": ["桜", "猫", "電車"],
        "三つの言葉の暗唱": ["桜", "猫", "電車"],
        "居場所": ["病院", "教習所", "自宅"],
        "100引く7": ["93"],
        "93引く7": ["86"],
        "年月日曜日": [],
        "3、5、2、9の逆唱": ["9253"],
        "2、8、6の逆唱": ["682"],
        "知っている野菜": []
    }

    def __init__(self):
        super().__init__()
        self.slot_calc = {
            "年齢": super().calc_age,
            "居場所": super().calc_location,
            "年月日曜日": super().calc_now,
            "三つの言葉の復唱": super().calc_memory,
            "三つの言葉の暗唱": super().calc_memory2,
            "100引く7": super().calc_subtraction,
            "93引く7": super().calc_subtraction,
            "2、8、6の逆唱": super().calc_reverse,
            "3、5、2、9の逆唱": super().calc_reverse,
            "知っている野菜": super().calc_vege,
        }

    def __call__(self, slots={}):
        slot_score = {}
        for slot, calc in self.slot_calc.items():
            if slot in slots.keys():
                if slots.get(slot, "") == None:
                    continue
                ans = slots.get(slot, "")
                slot_score[slot] = calc(ans, self.slot_correct.get(slot, []))
        
        return slot_score
    
    def set_refer_data(self, user_data):
        self.slot_correct["居場所"] = user_data["居場所"]
        self.slot_correct["年月日曜日"] = user_data["年月日曜日"]
        self.slot_correct["年齢"] = user_data["年齢"]

if __name__=="__main__":
    hdsr = HDSR()
    slots = {
        "年月日曜日": "2023年12月16日土曜"
    }
    score = hdsr(slots)
    print(score)
