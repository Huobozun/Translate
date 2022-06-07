
import nltk
from nltk import FreqDist

def _myfreq(text,label):
    
    text0=nltk.word_tokenize(text)
    s=len(text0)
    
    num=[]
    for i in range(0,len(label)):
       
        lines0=nltk.word_tokenize(label[i])
        x=len(lines0)
         #标签拼接
        searchlabel=''
        for i in range(0,x):
            searchlabel+=lines0[i].lower()

        #整篇拼接
        tokenstr=[]
        for i in range(0,s-x+1):
            longword=''
            for j in range(0,x):
                longword+=text0[i+j].lower()
            tokenstr.append(longword)
        
        fdist=FreqDist(tokenstr)

        num.append(int(fdist.freq(searchlabel)*len(text0)))
        #print(int(fdist.freq(i)*len(text0))) 
    return num#返回[4，1，...]


