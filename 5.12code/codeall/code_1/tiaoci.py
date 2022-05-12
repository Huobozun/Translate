import csv
import nltk
import http.client
import hashlib
from urllib import parse
import random
import time,re
import myfre
import re

#将要翻译的字符串合并
def _tiaocihebing(label):
    resu=''
    for i in range(0,len(label)):
        resu+=label[i]+';;;'
    return resu

#将合并的翻译结果分离
def _tiaocifenli(label):
    word=''
    resu=[]
    i=0
    while(i<len(label)):
        if(label[i]==';'and label[i+1]==';'and label[i+2]==';'):
            resu.append(word)
            word=''
            i+=1
        else:
            word+=label[i]
            i+=1
    return resu

            



#去除一个list中重复的词
def _tiaocichongfu(label):
    x=len(label)
    label1=[]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
        else:
            p=0
            for j in range(0,len(label1)):
                if(label1[j]==label[i]):
                    p=1
                    break
                else:
                    p=0
            if(p==0):
                label1.append(label[i])
    return label1

def _tiaocibold(label):#将只有大小写不同的剔除出去
    x=len(label)
    label1=[]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
        else:
            p=0
            for j in range(0,len(label1)):
                if(label1[j].lower()==label[i].lower()):
                    p=1
                    break
                else:
                    p=0
            if(p==0):
                label1.append(label[i])
    return label1

def _tiaociss(label):#将存在复数的剔除出去
    x=len(label)
    label1=[]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
        else:
            bp=0
            for j in range(0,len(label1)):
                if(len(label1[j])==len(label[i])):
                    lines0=nltk.word_tokenize(label1[j])
                    lines1=nltk.word_tokenize(label[i])
                    if(len(lines0)==len(lines1)):
                        xl=len(lines0)
                        bpx=0
                        for p in range(0,xl):
                            if(lines0[p].lower()==lines1[p].lower() or lines0[p].lower()+'s'==lines1[p].lower() or lines0[p].lower()==lines1[p].lower()+'s'):
                                bpx+=1
                        if(bpx==xl):
                            bp=1
                            break
                        else:
                            bp=0    
                    else:
                        bp=0
                else:
                        bp=0
            if(bp==0):
                label1.append(label[i])
    return label1

def _tiaocisuo(label):#将不用翻译的缩写提取出来，单独放在labelsuo
    x=len(label)
    label1=[]
    labelsuo=[]
    for i in range(0,x):
        if(label[i].isupper()==True):
            xlabel=''
            xlabel=label[i]
            p=0
            for j in range(0,len(xlabel)):
                if(xlabel[j]==' '):
                    p=1
            if(p==0):
                labelsuo.append(label[i])
            else:
                label1.append(label[i])
        else:
            label1.append(label[i])
    return label1,labelsuo

def _tiaocitong(label):#查找可以由其他词条的翻译结果推断出来的词条，并给出对应词条index和本词条的对应位置（0，（2,15））
    line=label
    x=len(label)
    _res=[]
    for i in range(0,len(line)):
        x=line[i]
        if(i==0):
            _res.append('Y')
        else:
            for j in range(0,i):
                #m = re.search(x,line[j])
                print('1',x)
                print('2',line[j])
                n = re.search(line[j],x)
                if(n!=None):
                    #print(i,(j,n.span()))
                    _res.append((j,n.span()))
                    break
                else:
                   # print('NONE')
                    _res.append('Y')
                
        
    return _res