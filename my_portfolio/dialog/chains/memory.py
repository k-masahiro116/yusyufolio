import json

from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_from_dict
# 会話をしたりメモリから文脈を読み込むチェーン
from langchain.chains import LLMChain

class Memory(LLMChain):
    WINDOW_SIZE = 15
    memory_chat = ConversationBufferWindowMemory(k=WINDOW_SIZE, ai_prefix="ワンコ", human_prefix="ユーザ")
        
    def dialog_load(self, chat_history=[], path=""):
        if chat_history != []:
            self.memory_chat.chat_memory.messages = chat_history[-self.WINDOW_SIZE:]
        if path != "":
            try:
                with open(path, 'r') as f:
                    chat_history = messages_from_dict(json.load(f))
            except (json.decoder.JSONDecodeError, TypeError, FileNotFoundError):
                chat_history = []
            self.memory_chat.chat_memory.messages = chat_history

    def add_user_message(self, message: str) -> None:
        self.memory_chat.chat_memory.add_user_message(message)
        
    def add_ai_message(self, message: str) -> None:
        self.memory_chat.chat_memory.add_ai_message(message)