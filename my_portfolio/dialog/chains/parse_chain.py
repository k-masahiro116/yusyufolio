import os, time
import openai
# チャットモデルのラッパーをインポート
import langchain
from langchain import OpenAI
from langchain.prompts import PromptTemplate
# 会話をしたりメモリから文脈を読み込むチェーン
from dialog.chains.memory import Memory
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()

class Parse(Memory):
    def __init__(self):
        llm = OpenAI(temperature=0)
        template = """
            一度深呼吸をしてください。
            ユーザの対話履歴から単語を抜き出し、以下の項目に割り当ててください。
            割り当てられるものがない場合は、項目は空白でも構いません。
            ただし、ワンコの発話内容から項目を埋めてはいけません。

            項目
            名前:
            年齢:
            年月日曜日:
            居場所:
            三つの言葉の復唱:
            100引く7:
            93引く7:
            2、8、6の逆唱:
            3、5、2、9の逆唱:
            三つの言葉の暗唱:
            知っている野菜:

            対話履歴
            {history} 

            =>"""
        prompt = PromptTemplate(
            input_variables=["history"],
            template=template
        )
        super().__init__(llm=llm, prompt=prompt)
        
    def run(self, history="こんにちは"):
        response = "無し"
        try_count = 3
        for try_time in range(try_count):
            try:
                response = self.predict(history=history)
            except (openai.InvalidRequestError, openai.OpenAIError):
                    time.sleep(1)
        return response.strip()
    
