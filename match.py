
#Mrs., Mr., Ms., Prof., Dr., Gen., Rep., Sen., St., A.M. P.M.

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
    
    
print match("example","com")    ,True
print match("example"," hello") ,False
print match("Mr"," James") ,True
print match("Mrs"," Lark") ,True
print match("Ms"," Helen") ,True 
print match("Dr"," Helen") ,True
print match("Ms"," Helen") ,True
print match("Ph","D") ,True
print match("D"," degree") ,True
print match("U","S") ,True 


