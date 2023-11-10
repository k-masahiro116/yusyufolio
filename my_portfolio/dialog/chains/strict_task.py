import json, time

import openai
# チャットモデルのラッパーをインポート
from langchain.chat_models import ChatOpenAI
# チャット履歴のラッパーをインポート
from langchain.memory import ConversationBufferMemory
# 会話をしたりメモリから文脈を読み込むチェーン
from langchain.chains import ConversationChain
from langchain.schema import messages_to_dict, messages_from_dict
# チャットプロンプト用のテンプレートをインポート
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder, 
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


template = """
        AIは以下の条件を元にstep-by-stepでユーザスロットを埋めていきます
        
        1. ユーザの発話に「診断して」または「認知症診断をして」という要求があったとき、質問を開始する。
        2. AIはユーザに対して、1問ずつ会話形式で質問をする。(対話履歴を参考にする)
        3. 2の質問で得られた回答を元にユーザスロットを一つずつ順番に埋める。
        4. 会話で得られた情報を元にユーザスロットに埋めていく。
        5. ユーザの発話が聞き返しやスキップなどに該当する場合、それに応じた遷移をする。
        6. 分からないと言われた場合、ヒントを教えるか、次の問題に移る。
        
        前提条件
        6と8のユーザスロットは、それぞれ5と7のユーザスロットが正解だったときのみ埋める必要がある。
        
        ユーザスロット
        1. 年齢
        2. 今日の年,月,日,曜日
        3. ユーザが現在居る場所
        4. 三つの言葉の復唱(桜、猫、電車)
        5. 100引く7の計算
        6. 93引く7の計算
        7. 次の数字を逆唱(2、8、6)
        8. 次の数字を逆唱(3、5、2、9)
        9. 復唱した三つの言葉を覚えているか
        10. 知っている野菜をできるだけ多く答えてもらう(10個を超えたら終了)
    """

class StrictTask(ConversationChain):
    topic = "HDS-R"
    hdsr_path = "dialog/assets/json/history/hdsr_history.json"
    results_path = 'dialog/assets/json/results/hdsr.json'
    topics = ["HDS-R"]
    def __init__(self, topic=topic):
        llm = ChatOpenAI(temperature=0)
        memory = ConversationBufferMemory(return_messages=True, ai_prefix="ワンコ", human_prefix="ユーザ")
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template=template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])

        super().__init__(llm=llm, memory=memory, prompt=prompt)
        self.dialog_load()
        
    def run(self, command="お願いします"):
        try_count = 3
        response = ""
        for try_time in range(try_count):
            try:
                response = self.predict(input=command)
                break
            except openai.InvalidRequestError:
                #生成する文が長文だったため制限が来た。履歴をpopして回避
                self.memory.chat_memory.messages.pop(0)
                self.memory.chat_memory.messages.pop(0)
            except (openai.OpenAIError, ConnectionError):
                time.sleep(2)
                
        if "正解です" in response:
            response = response.replace("正解です。", "")
        return response
        
    def dialog_load(self, path=hdsr_path):
        try:
            with open(path, 'r') as f:
                chat_history = messages_from_dict(json.load(f))
        except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
            chat_history = []
        self.memory.chat_memory.messages = chat_history
        
    def dialog_save(self, path=results_path):
        # 最後に、実際に会話した内容が memory オブジェクトに保持されていることを確認します
        history = self.memory.chat_memory
        with open(path, 'w') as f:
            json.dump(messages_to_dict(history.messages), f, indent=2, ensure_ascii=False)
    
