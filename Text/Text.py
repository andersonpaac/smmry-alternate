# sompar = Text.paras[0] -> para object
# sent = sompar.sentences[0] -> sentence object
# sent.score, sent.text, sent.belongs -> para number
from Sentences import Sentence
from Constants import Constant
import datetime
from collections import OrderedDict
import collections
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import numpy as np
np.set_printoptions(threshold='nan')


const = Constant.constant()

'''
    xxxxxxx Mr. Douglas                 Direct match
    xxxxxxxx Mrs. Douglas               Direct match
    xxxxxxx Ms. Douglas                 Direct match
    
    
    xxxxxxxx Peter A. Douglas           Capital before

    
    example.com is                      Spaces
    U.S.A                               Spaces
    
    
    xxxxxx. xxxxxx

'''

#Returns true when it's not a line end.
def match(line1, line2=""):
    if line1[-2:].lower() == "mr" or line1[-2:].lower() == "ms" or line1[-3:].lower() == "mrs":
        return True
    if line1[-2:].lower() == "dr":
        return True
    if line1[-1].upper() == line1[-1]:
        return True
    if line2 != "":
        if line2[0] != " ":
            return True
    return False
        
class text:
    def __init__(self, text):
        self.rawtext = text
        self.numparas = const.UNSET
        self.sentences = []
        self.isContextBuilt = False
        self.frequencies = {}
        self.stopwords = []
        self.graph = np.array([])
        self.isDepBuilt = False
        self.isScoreBuilt = False
        self.score = {}
        self.summary = ""
        self.initstopwords()
        
    
    def initstopwords(self):
        try:
            s=set(stopwords.words('english'))
        except LookupError as e:
                import nltk
                nltk.download()
                s=set(stopwords.words('english'))
        st = LancasterStemmer()
        for each in s:
            self.stopwords.append(st.stem(each))
    
    #Given a dictionary of key: frequency, value: array of words
    #build the opposite
    def buildFreqDict(self):
        self.freqDict = {}
        if not self.isContextBuilt:
            self.buildContext()
        for frequency in self.frequencies:
            words = self.frequencies[frequency]
            for word in words:
                self.freqDict[word] = frequency
            
            
    def buildMatrix(self, shape):
        arr = np.zeros(shape[0] * shape[1])
        arr.shape = (shape[0], shape[1])
        arr.fill(0)
        return arr
        
    def printSummary(self, limit):
        keys = self.score.keys()
        keys.reverse()
        if len(keys) > limit:
            for i in xrange(limit):
                vs = self.score[keys[i]]
                self.summary = self.summary + "\n" + self.sentences[vs[0]].rawtext
        print self.summary
    
    
    def getSMMRY(self, limit=5):
        self.buildSMMRY()
        self.printSummary(limit)
        
    def buildSMMRY(self):
        self.buildFreqDict()
        self.score = {}
        for i in xrange(len(self.sentences)):
            score = self.sentences[i].setFreqScore(self.freqDict)
            if score in self.score:
                self.score[score].append(i)
            else:
                self.score[score] = [i]
            self.score = collections.OrderedDict(sorted(self.score.items()))
            self.isScoreBuilt = True
            
        return self.score
            
            
    def getSummary(self,limit=5):
        self.buildDependencyGraph()
        self.buildScore()
        self.printSummary(limit)
    
    def buildScore(self):
        if not self.isScoreBuilt:
            self.score = {}
            if not self.isDepBuilt:
                self.buildDependencyGraph()
            for i in xrange(len(self.sentences)):
                sc = np.sum(self.graph[i])
                if sc in self.score:
                    self.score[sc].append(i)
                else:
                    self.score[sc] = [i]
            self.score = collections.OrderedDict(sorted(self.score.items())) 
            self.isScoreBuilt = True
            
        return self.score
            
        
    def buildDependencyGraph(self):
        if not self.isDepBuilt:
            self.graph = self.buildMatrix([len(self.sentences),len(self.sentences)])
            
            print "Graph shape is: "+ str(self.graph.shape)
            for i in xrange(len(self.sentences)):
                for j in xrange(len(self.sentences)):
                    if i!=j:
                        if self.graph[i][j] == 0.0:
                            self.graph[i][j] = self.sentintersect(self.sentences[i], self.sentences[j])  
                            self.graph[j][i] = self.graph[i][j] 
                    j = j+ 1
                i = i + 1
            self.isDepBuilt = True
        return self.graph
        
    def parseSentences(self):
        dat = self.rawtext.split("\n")
        raw_sentences = []
        counter = 0
        senttouse = ""
        for each in dat:
            if senttouse != "":
                self.sentences.append(Sentence.sentence(senttouse), self.stopwords)
                counter = counter + 1
            nlines = each.split(".")
            middleof = False
            senttouse = ""
            i = 0
            while i < (len(nlines)):
                if i+1 < len(nlines):
                    eval = match(nlines[i], nlines[i+1])

                else:
                    eval = False     
                
                if eval: 
                    if middleof:
                        senttouse = senttouse + "."+ nlines[i]       # Mr.Lark and Mr. Pork ar meeting today.
                    else:                                            # cfcfcffggh and Mr. Pork ar meeting today.
                        middleof = True
                        senttouse = nlines[i]
                else:
                    if middleof:
                        senttouse = senttouse + "." + nlines[i] + "."
                    else:
                        senttouse = nlines[i] + "."
                    if len(senttouse) > 2:
                        self.sentences.append(Sentence.sentence(senttouse, self.stopwords))
                    counter = counter + 1
                    middleof = False
                    senttouse = ""
                
                i = i + 1
                
    #Collection to put in order (auto-sort)
    def reverseDict(self):
        ndict = OrderedDict()
        for each in self.frequencies:
            count = self.frequencies[each]['freq']
            if count in ndict:
                ndict[count].append(each)
            else:
                ndict[count] = [each]
        return collections.OrderedDict(sorted(ndict.items()))      
    
    
    def buildContext(self):
        if not self.isContextBuilt:
            for each in self.sentences:
                vals = each.buildContext()
                for each in vals:
                    if each in self.frequencies:
                        self.frequencies[each]['freq'] = self.frequencies[each]['freq'] + 1
                    else:
                        self.frequencies[each] = {"freq": 1}
            self.frequencies = self.reverseDict()
            self.isContextBuilt = True
    
    def debugTextGraph(self, fname=""):
        if fname == "":
            fname = "text-graph-"+str(datetime.datetime.now())+".txt"
        fd = open(fname, "wb")
        first = True
        if not self.isDepBuilt:
            self.buildDependencyGraph()
        fd.write(np.array_str(self.graph))
        fd.close()
    
    def debugTextScore(self, fname=""):
        if fname == "":
            fname = "text-score-"+str(datetime.datetime.now())+".txt"
        fd = open(fname, "wb")
        first = True
        if not self.isScoreBuilt:
            self.buildScore()
        first = False
        for each in self.score:
            if first:
                fd.write(str(each).ljust(40) + ":" + str(self.score[each]))
                first = False
            else:
                fd.write("\n"+ str(each).ljust(40) + ":" + str(self.score[each]))
        fd.close()
        
        
    def debugTextFreqToFile(self, fname = ""):
        if not self.isContextBuilt:
            self.buildContext()
        if fname =="":
            fname = "text-freq-"+str(datetime.datetime.now())+".txt"
        fd = open(fname, 'wb')
        first = True
        for each in self.frequencies:
            if first:
                fd.write(str(each).ljust(40)+"\t\t"+str(self.frequencies[each]))
                first = False
            else:
                fd.write("\n"+str(each).ljust(40)+ "\t\t"+str(self.frequencies[each]))
        fd.close()
        
    def debugSentencesToFile(self, fname = ""): 
        if fname == "":
            fname = "sentences-rawtext-"+str(datetime.datetime.now())+".txt"
        fd = open(fname, "wb")
        print "debugSentencestoFile: "+str(len(self.sentences)) + " sentences identified"
        first = True
        for each in self.sentences:
            if first:
                fd.write(each.rawtext)
                first = False
            else:
                fd.write("\n"+each.rawtext)
        fd.close()
    
    def debugSentenceContextToFile(self, fname =""):
        if fname =="":
            fname = "sentences-context-"+str(datetime.datetime.now())+".txt"
        fd = open(fname, 'wb')
        first = True
        for each in self.sentences:
            if first:
                fd.write(str(each.buildContext()))
                first = False
            else:
                fd.write("\n"+str(each.buildContext()))
        fd.close()
        
        
        
    def sentintersect(self, sent1, sent2):
        arr1 = sent1.rawTokens
        arr2 = sent2.rawTokens
        arr3 = list(set(arr1) & set(arr2))
        score = float(len(arr3))/((len(arr1)+len(arr2))/float(2))
        return score

    
    def amruthaSummary(self):
        count = 0
        score = [0.0 for i in xrange(len(self.sentences))]
        for sent in self.sentences:
                arr1 = sent.uniqueWords
                count2 = 0
                for sent2 in self.sentences:
                    if count != count2:
                        arr2 = sent2.uniqueWords
                        arr3 = list(set(arr1) & set(arr2))
                        score[count] = score[count]+(float(len(arr3))/((len(sent.uniqueWords)+len(sent2.uniqueWords))/float(2)))
                    count2 = count2 + 1
                count = count + 1    
        print score
        return score

    
    

#To Do
#4  -   Order & Print summary
#5  -   Chronological order

#Score Sentence Sentence_NU

# orderbyscore limit 3 order by chronology

'''
    def findsummary(self, arrscore):
    
'''
