#from Constants import Constant
from nltk.corpus import stopwords
import string
from nltk.stem.lancaster import LancasterStemmer
class sentence:

    def __init__(self, text, stopwords):
        self.rawtext = self.filter(text)
        self.uniqueWords = []
        self.isContextBuilt = False
        self.unicodeErrors = 0
        self.stopwords = stopwords
        self.rawTokens = []
        self.tokenizeRawText()
        
    
    def tokenizeRawText(self):
        for each in self.rawtext:
            st = LancasterStemmer()
            try:
                ev = st.stem(each.lower())
                self.rawTokens.append(ev)
            except UnicodeDecodeError as e:
                self.unicodeErrors = self.unicodeErrors + 1
                
    def setFreqScore(self, freqDict):
        self.score = 0
        for each in self.uniqueWords:
            if each in freqDict:
                self.score = self.score + freqDict[each]
        return self.score
        
    #Cleans raw input before saving
    def filter(self, text):
        return text.lstrip().rstrip()
        
    def buildContext(self):
        if self.isContextBuilt == False:
            sometext = self.rawtext.translate(None, string.punctuation)
            st = LancasterStemmer()
            sometext = sometext.split()
            for each in sometext:
                try:
                    ev = st.stem(each.lower())
                    if ev not in self.stopwords:
                        self.uniqueWords.append(ev)
                except UnicodeDecodeError as e:
                    self.unicodeErrors = self.unicodeErrors + 1
            self.isContextBuilt = True
        return self.uniqueWords