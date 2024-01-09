import time
import openai
# チャットモデルのラッパーをインポート
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
# 会話をしたりメモリから文脈を読み込むチェーン
from dialog.chains.memory import Memory
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
# set_llm_cache(InMemoryCache(database_path="langchain.db"))
set_llm_cache(InMemoryCache())

class Detector(Memory):
    def __init__(self):
        llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
        template = """
            一度深呼吸をしてください。
            AIは、直前の話題と対話履歴の対を元にして次の話題を推定します。
            また、直前の話題がHDS-Rのときは、中断または終了したいと言われるまで常にHDS-Rを次の話題とします。
            
            入出力例
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
        for _ in range(try_count):
            try:
                response = self.predict(pre_topic=topic, history=text)
                break
            except (openai.InvalidRequestError, openai.OpenAIError):
                time.sleep(1)
        return response.strip()
