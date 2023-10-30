from typing import Dict, List

# LLMChain のインポート
from langchain.chains import LLMChain

# カスタムチェーンを定義するために Chain クラスをインポート
from langchain.chains.base import Chain

#対話履歴を保持する機能を実装する
# このチェーンは、3つの LLMChain の出力を連結する
class ConcatChain(Chain):
    # もととなる3つの LLMChain をコンストラクタで受け取る
    detector: LLMChain
    wanco: LLMChain
    strict: LLMChain

    @property
    def input_keys(self) -> List[str]:
        return ["text", "volume"]

    @property
    def output_keys(self) -> List[str]:
        return ['output']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        text_input = inputs.get("text", "")
        self.detector.add_user_message(text_input)
        Topic = self.detector.run()
        if Topic in self.strict.topics:
            output = self.strict.run(text_input)
        else:
            output = self.wanco.run(inputs)
        self.detector.add_ai_message(output)
        return {"output": output}
    
    def dialog_load(self):
        chat_history = self.wanco.dialog_load()
        self.detector.dialog_load(chat_history=chat_history)
        
    def dialog_save(self):
        self.wanco.dialog_save()
    
    def dialog_summary(self):
        return self.wanco.dialog_summary()