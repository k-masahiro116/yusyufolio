import time
import openai
# チャットモデルのラッパーをインポート
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
# 会話をしたりメモリから文脈を読み込むチェーン
from dialog.chains.memory import Memory
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path="langchain.db"))

class Detector(Memory):
    def __init__(self):
        llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0)
        template = """
            一度深呼吸をしてください。
            AIは以下のような直前の話題と対話履歴の対を元に、次の話題を推定します。
            また、直前の話題がHDS-Rのときは、中断をしたいと言われるまで常にHDS-Rを次の話題とします。
            
            推定の例
            挨拶:今日の夕飯美味しかった =>食事
            HDS-R:24歳です。=>HDS-R
            HDS-R:自宅です =>HDS-R
            天気:最近あまり元気が出ない =>体調
            趣味:音楽聴いてると楽しい =>趣味
            HDS-R:玉ねぎトマト白菜ピーマン =>HDS-R
            趣味:わからない =>趣味
            HDS-R:終わりにして =>終了
            挨拶:おはよう =>挨拶
            HDS-R:中断してほしい =>中断
            挨拶:診断して =>HDS-R
            挨拶:診断してほしい =>HDS-R
            HDS-R:もう無いです =>終了
            
            上記の推定の例に従って、以下の直前の話題と対話履歴の対から次の話題を推定してください。
            {pre_intent}:{text} =>
            """
        prompt = PromptTemplate(
            input_variables=["pre_intent", "text"],
            template=template
        )
        super().__init__(llm=llm, prompt=prompt)
        
    def run(self, intent="挨拶", text="こんにちは"):
        response = "無し"
        try_count = 3
        for _ in range(try_count):
            try:
                response = self.predict(pre_intent=intent, text=text)
                break
            except (openai.BadRequestError, openai.OpenAIError) as e:
                print("OpenAI Error: {}".format(e))
                time.sleep(1)
        print(response.strip())
        return response.strip()
