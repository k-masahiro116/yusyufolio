from typing import Dict, List
from langchain.chains import LLMChain
from langchain.chains.base import Chain

class ConcatChain(Chain):
    detector: LLMChain
    chitchat: LLMChain
    strict: LLMChain
    intent = "挨拶"
    model = ""
    pre_model = ""

    @property
    def input_keys(self) -> List[str]:
        return ["text"]

    @property
    def output_keys(self) -> List[str]:
        return ['output']

    def _call(self, inputs):
        text = inputs.get("text", "")
        text = self.text_check(text)
        preintent = self.intent
        self.intent = self.detector.run(self.intent, text)
        self.pre_model = self.model
        if self.intent in self.strict.topics:
            if preintent != self.intent:
                self.strict.__init__(self.intent)
            self.model = "strict"
            output = self.strict.run(text, self.intent)
        elif preintent in self.strict.topics and ("中断" in self.intent or "終了" in self.intent):
            self.model = "strict"
            output = self.strict.run("終了して", self.intent)
            self.chitchat.dialog_load(reset=True)
            self.intent = "挨拶"
        else:
            self.model = "chitchat"
            output = self.chitchat.run(text)
        
        return {"output": output}
    
    def text_check(self, text):
        if text == "":
            return "ユーザが無言であるため、何か問いかけてください。"
        else:
            return text
        
    def dialog_load(self):
        self.strict.dialog_load()
        chat_history = self.chitchat.dialog_load(reset=True)
        self.detector.dialog_load(chat_history=chat_history)
        
    def dialog_save(self):
        self.chitchat.dialog_save()
    
    def dialog_summary(self):
        return self.chitchat.dialog_summary()