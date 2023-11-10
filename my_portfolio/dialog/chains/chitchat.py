import json, re, posixpath
import openai, openai.error
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.schema import messages_to_dict, messages_from_dict

# チャットプロンプト用のテンプレートをインポート
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder, 
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from ..sensors import Forecasts

WINDOW_SIZE = 5
class ChitChat(ConversationChain):
    posixpath.join("/media")
    conv_path = 'dialog/assets/json/history/conversation.json'
    view_path = 'dialog/assets/json/history/viewable_conversation.json'
    sum_path = 'dialog/assets/text/summary.txt'
    viewable_memory = ConversationBufferMemory(return_messages=True, ai_prefix="ワンコ", human_prefix="ユーザ")
    nextTopic = ""
    template = """
        あなたの名前はワンコです。
        ワンコの情報: 2023年5月27日に電気通信大学の沼尾研究室で生まれた。色んな人とお話しするのが好き。
        ワンコの語尾: わん！
        ワンコの性格: 自然かつ親密な会話をするが、返答は短めです。
        ワンコの話し方: option情報を予備知識として、utteranceへの返答を出力します。
        ワンコの目的: ユーザについての情報を集めることに努めます。
        ワンコの主なトークテーマ: 天気、食事、予定、睡眠の質、体調、趣味、名前
        ワンコは、質問の答えを知らない場合、正直に「知らない」と答えます。
        option情報については、ユーザは認知していないので注意してください。
        
        以下はユーザのデータ
        {}"""
    def __init__(self, template=template, knowledge=True, ai_prefix="ワンコ", human_prefix="ユーザ"):
        llm = ChatOpenAI(temperature=0.4)
        memory = ConversationBufferWindowMemory(k=WINDOW_SIZE, return_messages=True, ai_prefix=ai_prefix, human_prefix=human_prefix)
        if knowledge == True:
            template = template.format(self.summary_load())
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        super().__init__(llm=llm, memory=memory, prompt=prompt)
        
    def run(self, command, nextTopic="挨拶",json_cc=True):
        self.nextTopic = nextTopic
        if json_cc == True:
            input_text = command.get("text", "")
            utter_json = self.__preprocess(command)
        else:
            input_text = command
        trycount = 3
        response = "スヤスヤ"
        for _ in range(trycount):
            try:
                if json_cc == True:
                    response = self.predict(input=json.dumps(utter_json))
                else:
                    response = self.predict(input=input_text)
                break
            except openai.InvalidRequestError:
                self.memory.chat_memory.messages.pop(0)
                self.memory.chat_memory.messages.pop(0)
            except (openai.error.RateLimitError,openai.OpenAIError, openai.error.ServiceUnavailableError):
                break
        self.__memory_edit(input=input_text, response=response)
        return response
    
    def __preprocess(self, command):
        text = command.get("text", "")
        volume = command.get("volume", 65)
        if text == "":
            if 50 > volume:
                self.nextTopic = "ユーザの声が小さくて聞き取れない"
            else:
                self.nextTopic = "ユーザの声が聞き取れない"
        return {"utterance": text, "option": {"weather": Forecasts().weather}}
        
    def __memory_edit(self, input, response):
        self.viewable_memory.chat_memory.add_user_message(input) 
        self.viewable_memory.chat_memory.add_ai_message(response) 
        
    def dialog_load(self, path1=conv_path, path2=view_path, reset=False):
        try:
            with open(path1, 'r') as f:
                chat_history = messages_from_dict(json.load(f))
        except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
            chat_history = []
        if not reset:
            self.memory.chat_memory.messages = chat_history[-WINDOW_SIZE:]
        try:
            with open(path2, 'r') as f:
                chat_history = messages_from_dict(json.load(f))
        except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
            chat_history = []
        self.viewable_memory.chat_memory.messages = chat_history
        return chat_history
        
    def summary_load(self, path=sum_path):
        with open(path, 'r') as f:
            chat_summary = f.read()
        return chat_summary
        
    def dialog_save(self, path1=conv_path, path2=view_path):
        # 最後に、実際に会話した内容が memory オブジェクトに保持されていることを確認します
        history = self.memory.chat_memory.messages
        try:
            with open(path1, 'w') as f:
                json.dump(messages_to_dict(history), f, indent=2, ensure_ascii=False)
        except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
            pass
        history = self.viewable_memory.chat_memory.messages
        try:
            with open(path2, 'w') as f:
                json.dump(messages_to_dict(history), f, indent=2, ensure_ascii=False)
        except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
            pass
        
    def dialog_summary(self, path=sum_path):
        command="""対話内容からユーザについての重要な情報だけ抽出し、RDF tripleの形式でデータ化してください。
                    下記にその例を示す。
                    <ユーザ, 好きな食べ物, いちご>
                    <ユーザ, 今日の天気, 晴れ>
                    """
        response = self.predict(input=command)
        sum_list = list(set(re.findall("\<.*?\>", response) + re.findall("\<.*?\>", self.summary_load())))
        with open(path, 'w') as f:
            for l in sum_list:
                f.write(l)
        return sum_list
                
    #llmを用いたsummaryの出力
    def dialog_summary_chain(self):
        memory = ConversationSummaryMemory(llm=self.llm, return_messages=True)
        messages = self.memory.chat_memory.messages
        previous_summary = ""
        sum = memory.predict_new_summary(messages, previous_summary)
        print(sum)
        