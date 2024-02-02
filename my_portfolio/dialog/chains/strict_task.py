import json, time
import random as r
import openai
# チャットモデルのラッパーをインポート
from langchain_openai import ChatOpenAI
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

scenarios = {
    "HDS-R": {
        "path": "dialog/assets/json/history/hdsr_history.json",
        "template" : """
        AIは以下の条件を元にstep-by-stepでユーザスロットを埋めていきます
        
        1. ユーザの発話に「診断して」または「認知症診断をして」という要求があったとき、質問を開始する。
        2. AIはユーザに対して、1問ずつ会話形式で質問をする。(対話履歴を参考にする)
        3. 2の質問で得られた回答を元にユーザスロットを一つずつ順番に埋める。
        4. 会話で得られた情報を元にユーザスロットに埋めていく。
        5. ユーザの発話が聞き返しやスキップなどに該当する場合、それに応じた遷移をする。
        6. 分からないと言われた場合、ヒントを教えるか、次の問題に移る。
        
        前提条件
        6のユーザスロットは、5のユーザスロットが正解だったときのみ埋める。
        8のユーザスロットは、7のユーザスロットが正解だったときのみ埋める。
        
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
        10. 知っている野菜をできるだけ多く答えてもらう
    """},
    "QUIZ": {
        "path": "dialog/assets/json/history/nazo_history.json",
        "template" : """
        AIはユーザに対して以下のクイズを出します。
        ユーザの回答がクイズの答えと合致しない場合は不正解とします。
        ユーザにヒントを聞かれたら柔軟に対応します。
        ユーザが無言だった場合は、ヒントを教えるかユーザに質問をします。
        クイズが終わったら、次のクイズするかユーザに質問します。
        
        クイズ=> {quiz}
        クイズの答え=> {answer}
        """
    }
}

class StrictTask(ConversationChain):
    TEMPLATE = "template"
    PATH = "path"
    topic = "HDS-R"
    topics = ["HDS-R", "QUIZ"]
    quiz_path = "dialog/assets/json/quiz/aio_04_dev_v1.0.jsonl"
    scenario = {}
    def __init__(self, topic=topic):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo" ,temperature=0)
        memory = ConversationBufferMemory(return_messages=True, ai_prefix="ワンコ", human_prefix="ユーザ")
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template=self.temp_load(topic)),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        super().__init__(llm=llm, memory=memory, prompt=prompt)
        self.scenario = scenarios.get(topic)
        self.dialog_load()
        
    def run(self, command="お願いします", topic = topic):
        try_count = 3
        response = ""
        input_text = self.quiz_process(command, topic)
        for try_time in range(try_count):
            try:
                response = self.predict(input=input_text)
                self.memory.chat_memory.messages.pop(0)
                break
            except openai.BadRequestError:
                #生成する文が長文だったため制限が来た。履歴をpopして回避
                self.memory.chat_memory.messages.pop(0)
            except (openai.OpenAIError, ConnectionError):
                time.sleep(2)
        if topic == "HDS-R":
            response = self.hdsr_process(response)
        return response
        
    def temp_load(self, topic=topic):
        if topic == "QUIZ":
            temp = self.quiz_load()
        else:
            scenario = scenarios.get(topic)
            temp = scenario.get("template")
        return temp
        
    def hdsr_process(self, response):
        if "正解" in response:
            response = response.replace("正解です。", "")
            response = response.replace("正解です。", "")
            response = response.replace("正解は93です。", "")
        if "AI: " in response:
            response = response.replace("AI: ", "")
        return response
    
    def quiz_process(self, command, topic):
        if topic == "QUIZ":
            if "次のクイズ" in command or "はい" in command or "次の問題" in command:
                self.__init__(topic="QUIZ")
                return "クイズしてほしい"
        return command
        

    def quiz_load(self, path=quiz_path):
        scenario = scenarios.get("QUIZ")
        template = scenario.get("template")
        with open(path) as f:
            jsonl_data = [json.loads(l) for l in f.readlines()]
            
        nazo = jsonl_data[r.randrange(len(jsonl_data))]
        quiz = nazo.get("question", "")
        answer = ", ".join(nazo.get("answers"))
        return template.format(quiz=quiz, answer=answer)
        
        
    def dialog_load(self):
        path = self.scenario.get(self.PATH)
        if path==None:
            return
        try:
            with open(path, 'r') as f:
                chat_history = messages_from_dict(json.load(f))
        except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
            chat_history = []
        self.memory.chat_memory.messages = chat_history
    