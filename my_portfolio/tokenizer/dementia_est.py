import math
import collections
import pandas as pd
import numpy as np
import tokenizer.main_func as mf

import CaboCha

cabocha = CaboCha.Parser('-n1')

#ここに原因がある(連体化と副詞化が表示されない理由)
def parse_sentense(sentense_str, sentense_begin):
    feats = []
    tree = cabocha.parse(sentense_str)

    offset = sentense_begin

    text = sentense_str
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        chunk_begin = None

        for j in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
            token = tree.token(j)
            features = token.feature.split(",")
            token_begin = text.find(token.surface) + offset
            token_end = token_begin + len(token.surface)
            if chunk_begin is None or "連体化" in features or "副詞化" in features or "連語" in features:
                chunk_begin = token_begin
                feats.append(features)
    return feats



def n_gram_word(target, n):
    # 基準を1文字(単語)ずつ ずらしながらn文字分抜き出す
    return [ target[idx:idx + n] for idx in range(len(target) - n + 1)]

def get_ngram(text, n):
    l = []
    n_gram = {}
    target = text.split(' ')
    for t in target:
        l = l + n_gram_word(t, n)
    n_gram = collections.Counter(l)
    return n_gram

def honores_static(nouns):
    #Nは名詞数
    N = mf.dict_sum(nouns)
    #Nuniは一回のみ使用される名詞
    Nuni = mf.filter_dict_len(nouns, v=1)
    #Uは名詞のタイプ数
    U = len(nouns)
    if N == 0 or U == 0 or 1-Nuni/U == 0 :
        return 0
    HS = 100*math.log(N/(1-Nuni/U))
    return HS

def brunets_index(nouns):
    #Nは名詞数
    N = mf.dict_sum(nouns)
    if N == 0:
        return 0
    #Uは名詞のタイプ数
    U = len(nouns)
    BI = math.pow(N, math.pow(U, -0.165))
    return BI
    
def type_token_ratio(token_each):
    type_sum = len(token_each)
    token_sum = mf.dict_sum(token_each)
    if token_sum == 0:
        return 0
    ttr = type_sum/token_sum
    return ttr

def vocabrary_level(noun_each):
    goi = pd.read_csv("./tokenizer/goi_4kohan_ijo_noun.csv", encoding="utf-8")
    goi_sum = 0
    for noun, num in noun_each.items():
        if noun in goi["標準的な表記"].tolist():
            goi_sum = goi_sum + num
    if mf.dict_sum(noun_each) == 0:
        return 0
    return goi_sum/mf.dict_sum(noun_each)
    
#最大値、最小値、平均値
def potential_vocabulary_size(tokens):
    ttp_l = pd.read_csv("./tokenizer/token_type_pvs.csv", encoding = "shift-jis")
    token_sum = mf.dict_sum(tokens)
    if token_sum == 0:
        return [0]
    type_sum = len(tokens)
    ttp_l2 = ttp_l[ttp_l["token"].isin([token_sum])]
    pvs = ttp_l2[ttp_l2["type"].isin([type_sum])]
    return pvs["pvs"].tolist()
    
class Est_Dementia:
    pos_features = [["動詞"],["自立"]]
    token_features = {
        "助詞": ["色々"],
        "動詞": ["やる"],
    }
    token_features2 = ["いう"]
    char_features = ["ね"]
    statistics_features = ["HS", "BI", "VL", "TTR"]
    pvs_features = ["PVS_AVG"]
    
    def __init__(self, text):
        self.text = text
        self.pos_rate = {}
        self.get_pos_data()
        for i, pos_f in enumerate(self.pos_features):
            for pos in pos_f:
                self.pos_rate[pos] = self.pos_freq([pos], pos_type=i)[pos]
        tfd1, self.scores1 = self.token_freq_pos()
        tfd2, self.scores2 = self.token_freq()
        tfd3, self.scores3 = self.ngram_freq()
        nouns = self.token_example()
        tokens = self.token_count()
        self.HS = honores_static(nouns)
        self.BI = brunets_index(nouns)
        self.VL = vocabrary_level(nouns)
        self.TTR = type_token_ratio(tokens)
        self.PVS = potential_vocabulary_size(tokens)
        # print(self.pos_rate, tfd1, tfd2, tfd3, {"HS": self.HS, "BI": self.BI, "VL": self.VL, "TTR": self.TTR, "PVS": self.PVS}, sep="\n")
        
    def __call__(self):
        self.data_x = np.array(list(self.pos_rate.values())+self.scores1+self.scores2+self.scores3+[self.HS, self.BI, self.VL, self.TTR]+self.PVS)
        result = mf.estimate("RF", self.data_x.reshape(1, -1))[0]
        judge = "認知症予備軍" if result[0] == 1 else "健常者"
        return judge
        
    def get_pos_data(self):
        self.pos_each = [{}, {}, {}]
        feats = parse_sentense(self.text, 0)
        for features in feats:
            for i, pe in enumerate(self.pos_each):
                if features[i] in pe.keys():
                    self.pos_each[i][features[i]] += 1
                else:
                    self.pos_each[i][features[i]] = 1
        
    def pos_freq(self, poss=["名詞"], pos_type = 1):
        pos_d = self.pos_each[pos_type]
        result = mf.dict_init(poss)
        for pos in result.keys():
            if pos in pos_d:
                if mf.dict_sum(pos_d) == 0:
                    result[pos] == 0
                else:
                    result[pos] = pos_d[pos]/mf.dict_sum(pos_d)
        return result
    
    #全単語数におけるngramの割合
    def ngram_freq(self):
        results = {}
        scores = list()
        for token in self.char_features:
            if token in results.keys(): continue
            ngram = get_ngram(self.text, len(token))
            if mf.dict_sum(ngram) == 0:
                score = 0
            else:
                score = ngram[token]/mf.dict_sum(ngram)
            results[token] = score
            scores = scores + [score]
        return results, scores
    
    #全単語数におけるtokenの割合
    def token_freq(self):
        results = {}
        scores = list()
        tokens_n = mf.dict_sum(self.pos_each[1])
        if tokens_n == 0:
            tokens_n = 1
        all_words = self.token_count()
        for token in self.token_features2:
            if token in results.keys(): continue
            token_n = mf.filter_dict_sum(all_words, k=token)
            score = token_n/tokens_n
            results[token] = score
            scores = scores + [score]
        return results, scores
    
    #pos中のtokenの割合
    def token_freq_pos(self):
        results = mf.dict_init(self.token_features.keys())
        scores = list()
        for pos, tokens in self.token_features.items():
            result = mf.dict_init(tokens)
            d = self.token_example(pos)
            for token in tokens:
                if mf.dict_sum(d) == 0:
                    score = 0
                else:
                    score = mf.filter_dict_sum(d, k=token)/mf.dict_sum(d)
                result[token] = score
                scores = scores + [score]
            results[pos] = result
        return results, scores
    
    #posのそれぞれの単語の数
    def token_example(self, pos="名詞"):
        token_example = {}
        feats = parse_sentense(self.text, 0)
        for features in feats:
            if pos in features[0] or pos in features[1]:
                if features[-3] in token_example.keys():
                    token_example[features[-3]] += 1
                else:
                    token_example[features[-3]] = 1
        return token_example
    
    def token_count(self):
        token_each = {}
        feats = parse_sentense(self.text, 0)
        for features in feats:
            if features[-3] in token_each.keys():
                token_each[features[-3]] += 1
            else:
                token_each[features[-3]] = 1
        return token_each
    


if __name__ == "__main__":
    text = ""
    EstD = Est_Dementia(text)
    print("認知機能評価の結果: ",EstD())