from typing import Dict, List
from langchain.chains import LLMChain
from langchain.chains.base import Chain

class ConcatChain(Chain):
    detector: LLMChain
    wanco: LLMChain
    strict: LLMChain
    topic = "挨拶"

    @property
    def input_keys(self) -> List[str]:
        return ["text", "volume"]

    @property
    def output_keys(self) -> List[str]:
        return ['output']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        text_input = inputs.get("text", "")
        self.detector.add_user_message(text_input)
        self.topic = self.detector.run(self.topic, text_input)
        if "中断" in self.topic or "終了" in self.topic:
            self.strict.__init__()
            output = "診断を終了しますワン。"
        elif "HDS-R" in self.topic:
            output = self.strict.run(text_input)
        else:
            output = self.wanco.run(inputs, nextTopic=self.topic)
        self.detector.add_ai_message(output)
        return {"output": output}
    
    def dialog_load(self):
        self.strict.dialog_load()
        chat_history = self.wanco.dialog_load(reset=True)
        self.detector.dialog_load(chat_history=chat_history)
        
    def dialog_save(self):
        self.wanco.dialog_save()
    
    def dialog_summary(self):
        return self.wanco.dialog_summary()