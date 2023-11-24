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
        text_input = inputs.get("text", "")
        self.detector.add_user_message(text_input)
        self.topic = self.detector.run(self.topic, text_input)
        self.pre_model = self.model
        if "HDS-R" in self.topic:
            self.model = "strict"
            output = self.strict.run(text_input)
            if "中断" in self.topic or "終了" in self.topic or "終了" in output:
                self.strict.__init__()
                self.topic = "挨拶"
        else:
            self.model = "chitchat"
            output = self.chitchat.run(text_input)
        
        self.detector.add_ai_message(output)
        return {"output": output}
    
    def dialog_load(self):
        self.strict.dialog_load()
        chat_history = self.chitchat.dialog_load(reset=True)
        self.detector.dialog_load(chat_history=chat_history)
        
    def dialog_save(self):
        self.chitchat.dialog_save()
    
    def dialog_summary(self):
        return self.chitchat.dialog_summary()