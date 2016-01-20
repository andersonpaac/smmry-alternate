# sompar = Text.paras[0] -> para object
# sent = sompar.sentences[0] -> sentence object
# sent.score, sent.text, sent.belongs -> para number

from Paras import Para
from Sentences import Sentence
from Constants import Constant

const = Constant.constant()
class text:
    def __init__(self, text):
        self.text = text
        self.numparas = Para.para("lmau")
    
    
    