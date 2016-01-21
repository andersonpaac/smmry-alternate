#open file and reads file, makes text obj, sets text.rawdata 
#python main.py -f sample-input-1.txt -o out.txt

from Constants import Constant
from Text import Text

fname = "sample-input-1.txtz"

def main():
    
    consts = Constant.constant()
    print consts.UNSET
    smmry = Text.text(readfromfile(fname))
    smmry.parseSentences()
    smmry.debugSentencesToFile()
    
    
def readfromfile(fname):
    fd = open(fname)
    dat = fd.read()
    fd.close()
    return dat
    

main()

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
    
      
    