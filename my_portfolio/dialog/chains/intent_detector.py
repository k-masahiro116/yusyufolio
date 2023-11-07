import time
import openai
# チャットモデルのラッパーをインポート
import langchain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
# 会話をしたりメモリから文脈を読み込むチェーン
from dialog.chains.memory import Memory
from langchain.cache import SQLiteCache
langchain.llm_cache = SQLiteCache(database_path="langchain_cache.db")

class Detector(Memory):
    def __init__(self):
        llm = OpenAI(temperature=0)
        template = """
            AIは以下のように対話履歴を元に現在の話題を推定します。
            また、診断中は常にHDS-Rを話題とする

            今日の夕飯美味しかった=>食事-夕方
            最近あまり元気が出ない=>体調-悪
            音楽聴いてると楽しい=>趣味-音楽
            診断してほしい=>HDS-R
            回答は以上になります=>HDS-R-終わり
            おはよう=>挨拶-朝
            こんにちは=>挨拶-昼
            中断してほしい=>中断
            {history}=>
        """
        prompt = PromptTemplate(
            input_variables=["history"],
            template=template
        )
        super().__init__(llm=llm, prompt=prompt)
        
    def run(self):
        history = self.memory_chat.load_memory_variables({})
        response = "無し"
        try_count = 3
        for try_time in range(try_count):
            try:
                response = self.predict(history=history)
            except (openai.InvalidRequestError, openai.OpenAIError):
                    time.sleep(1)
        return response.strip()
