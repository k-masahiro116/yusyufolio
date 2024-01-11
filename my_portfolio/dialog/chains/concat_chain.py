from typing import Dict, List
from langchain.chains import LLMChain
from langchain.chains.base import Chain

class ConcatChain(Chain):
    detector: LLMChain
    chitchat: LLMChain
    strict: LLMChain
    topic = "挨拶"
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
        self.detector.add_user_message(text)
        pretopic = self.topic
        self.topic = self.detector.run(self.topic, text)
        self.pre_model = self.model
        if "HDS-R" in self.topic:
            self.model = "strict"
            output = self.strict.run(text)
        elif "HDS-R" in pretopic and ("中断" in self.topic or "終了" in self.topic):
            self.model = "strict"
            output = self.strict.run("診断を終了して")
            self.strict.dialog_load()
            self.chitchat.dialog_load(reset=True)
            self.topic = "挨拶"
        else:
            self.model = "chitchat"
            output = self.chitchat.run(text)
        
        self.detector.add_ai_message(output)
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