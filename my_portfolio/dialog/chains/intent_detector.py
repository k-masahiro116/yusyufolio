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
            一度深呼吸をしてください。
            AIは以下のような直前の話題と対話履歴の対を元に次の話題を推定します。
            また、直前の話題がHDS-Rのときは、中断をしたいと言われるまで常にHDS-Rを次の話題とします。
            
            挨拶:今日の夕飯美味しかった =>食事
            天気:最近あまり元気が出ない =>体調
            趣味:音楽聴いてると楽しい =>趣味
            挨拶:おはよう =>挨拶
            HDS-R:中断してほしい =>中断
            挨拶:診断して =>HDS-R
            挨拶:診断してほしい =>HDS-R
            HDS-R:24歳です。=>HDS-R
            HDS-R:もうないです =>終了
            HDS-R:終わりにして =>終了
            HDS-R:自宅です =>HDS-R
            {pre_topic}:{history} =>"""
        prompt = PromptTemplate(
            input_variables=["pre_topic", "history"],
            template=template
        )
        super().__init__(llm=llm, prompt=prompt)
        
    def run(self, topic="挨拶", text="こんにちは"):
        response = "無し"
        try_count = 3
        for try_time in range(try_count):
            try:
                response = self.predict(pre_topic=topic, history=text)
            except (openai.InvalidRequestError, openai.OpenAIError):
                    time.sleep(1)
        return response.strip()
