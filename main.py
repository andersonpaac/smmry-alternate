#open file and reads file, makes text obj, sets text.rawdata 
#python main.py -f sample-input-1.txt -o out.txt

from Constants import Constant
from Text import Text

fname = "sample-input-1.txtz"

def main():
    consts = Constant.constant()
    smmry = Text.text(readfromfile(fname))
    smmry.parseSentences()
    smmry.debugSentencesToFile()
    smmry.debugSentenceContextToFile()
    smmry.debugTextFreqToFile()
    #smmry.getSummary()
    smmry.getSMMRY()


    
    
def readfromfile(fname):
    fd = open(fname)
    dat = fd.read()
    fd.close()
    return dat
    

main()

      

     