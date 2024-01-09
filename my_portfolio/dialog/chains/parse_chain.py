import os, time
import openai
# チャットモデルのラッパーをインポート
import langchain
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
# 会話をしたりメモリから文脈を読み込むチェーン
from dialog.chains.memory import Memory
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()

class Parse(Memory):
    def __init__(self):
        llm = OpenAI(model="text-davinci-003", temperature=0)
        template = """
            一度深呼吸をしてください。
            以下の手順をstep-by-stepで進めていきます。
            1. 対話履歴からユーザの対話履歴を抽出する
            2. 各項目に当たる情報をユーザの対話履歴から抽出し、割り当てる
            3. 割り当てた項目を全て出力する
            
            前提条件
            割り当てられるものがない場合は、項目は空白でも構わない。
            
            項目
            名前:
            年齢:
            年月日曜日:
            居場所:
            三つの言葉の復唱:
            三つの言葉の暗唱:
            100引く7:
            93引く7:
            2、8、6の逆唱:
            3、5、2、9の逆唱:
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
        for _ in range(try_count):
            try:
                response = self.predict(history=history)
                break
            except (openai.InvalidRequestError, openai.OpenAIError):
                    time.sleep(1)
        return response.strip()
    
