# sompar = Text.paras[0] -> para object
# sent = sompar.sentences[0] -> sentence object
# sent.score, sent.text, sent.belongs -> para number
from Sentences import Sentence
from Constants import Constant
import datetime
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
        
    def parseSentences(self):
        
        dat = self.rawtext.split("\n")
        raw_sentences = []
        counter = 0
        senttouse = ""
        for each in dat:
            if senttouse != "":
                self.sentences.append(Sentence.sentence(senttouse))
                counter = counter + 1
            nlines = each.split(".")
            middleof = False
            senttouse = ""
            i = 0
            while i < (len(nlines)):
                if counter == 30:
                    
                    print "---------------------------"
                    print "nlines[i] is "+ nlines[i]
                    print "middle of is" + str(middleof)
                    print "senttouse is "+senttouse
                    
                if i+1 < len(nlines):
                    eval = match(nlines[i], nlines[i+1])
                    if counter == 30:
                        print "Attempting to match - "+ nlines[i] + " AND "+nlines[i+1] + " RETURNED "+str(eval).upper()
                        print "----------------"
                        print "\n\n\n"

                else:
                    eval = False     
                
                if eval: 
                    if middleof:
                        senttouse = senttouse + "."+ nlines[i]       # Mr.Lark and Mr. Pork ar meeting today.
                    else:                                            # cfcfcffggh and Mr. Pork ar meeting today.
                        middleof = True
                        senttouse = nlines[i]
                else:
                    #nlines[i] is the end
                    if middleof:
                        senttouse = senttouse + "." + nlines[i] + "."
                    else:
                        senttouse = nlines[i].lstrip().rstrip() + "."
                    if len(senttouse) > 2:
                        self.sentences.append(Sentence.sentence(senttouse))
                    counter = counter + 1
                    middleof = False
                    senttouse = ""
                
                i = i + 1
                    
    def debugSentencesToFile(self, fname = ""): 
        if fname == "":
            fname = "sentences-"+str(datetime.datetime.now())+".txt"
        fd = open(fname, "wb")
        print "debugSentencestoFile: "+str(len(self.sentences)) + " sentences identified"
        for each in self.sentences:
            fd.write(each.rawtext+"\n")
    
        fd.close()

        



    

    def runscore(self):
        for each in self.sentences:
            each.setscore()
        
    

