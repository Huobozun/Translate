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
        resu+=label[i]+'\n'
    return resu
"""
#将合并的翻译结果分离
def _tiaocifenli(label):
    word=''
    resu=[]
    i=0
    while(i<len(label)):
        if(label[i]=='\n'):
            resu.append(word)
            word=''
            i+=1
        else:
            word+=label[i]
            i+=1
    return resu"""

"""def _tiaocihebing1(label):
    resu=''
    for i in range(0,len(label)):
        resu+='!'+label[i]+'>9,8'
    return resu

#将合并的翻译结果分离
def _tiaocifenli1(label):
    word=''
    resu=[]
    i=1
    while(i<len(label)):
        if(label[i]=='>' and label[i+1]=='9' and label[i+2]==',' and label[i+3]=='8'):
            resu.append(word)
            word=''
            i+=5
        else:
            word+=label[i]
            i+=1
    return resu            """




def _tiaocichongfu(label):#去除一个list中重复的词
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


def _tiaocichongfu1(label,type):#去除一个list中重复的词,并且合并type
    x=len(label)
    label1=[]
    type1=[]#类型由['','','']变为[['',''],['']]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
            if isinstance(type[i],str):
                type1.append([type[i]])
            else:
                type1.append(type[i])
        else:
            p=0
            for j in range(0,len(label1)):
                if(label1[j]==label[i]):
                    p=1
                    if isinstance(type[i],str):
                        type1[j].append(type[i])
                    else:
                        typepe=type[i]
                        for pp in range(0,len(typepe)):
                            type1[j].append(typepe[pp])
                    break
                else:
                    p=0
            if(p==0):
                label1.append(label[i])
                if isinstance(type[i],str):
                    type1.append([type[i]])
                else:
                    type1.append(type[i])            
    return label1,type1#保存除去相同的词条后剩下的词条list，以及合并后的type

def _tiaocichongfu2(label,type,resource):#去除一个list中重复的词,并且合并type和resource
    x=len(label)
    label1=[]
    type1=[]#类型由['','','']变为[['',''],['']]
    resource1=[]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
            if isinstance(type[i],str):
                type1.append([type[i]])
            else:
                type1.append(type[i])
            if isinstance(resource[i],str):
                resource1.append([resource[i]])
            else:
                resource1.append(resource[i])
        else:
            p=0
            for j in range(0,len(label1)):
                if(label1[j]==label[i]):
                    p=1
                    if isinstance(type[i],str):
                        type1[j].append(type[i])
                    else:
                        typepe=type[i]
                        for pp in range(0,len(typepe)):
                            type1[j].append(typepe[pp])
                    if isinstance(resource[i],str):
                        resource1[j].append(resource[i])
                    else:
                        resourcepe=resource[i]
                        for pp in range(0,len(resourcepe)):
                            resource1[j].append(resourcepe[pp])
                    break
                else:
                    p=0
            if(p==0):
                label1.append(label[i])
                if isinstance(type[i],str):
                    type1.append([type[i]])
                else:
                    type1.append(type[i])   
                if isinstance(resource[i],str):
                    resource1.append([resource[i]])
                else:
                    resource1.append(resource[i])         
    return label1,type1,resource1#保存除去相同的词条后剩下的词条list，以及合并后的type


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

def _tiaocibold1(label,type):#将只有大小写不同的剔除出去,并且合并type
    x=len(label)
    label1=[]
    type1=[]#类型由['','','']变为[['',''],['']]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
            if isinstance(type[i],str):
                type1.append([type[i]])
            else:
                type1.append(type[i])
        else:
            p=0
            for j in range(0,len(label1)):
                if(label1[j].lower()==label[i].lower()):
                    p=1
                    if isinstance(type[i],str):
                        type1[j].append(type[i])
                    else:
                        typepe=type[i]
                        for pp in range(0,len(typepe)):
                            type1[j].append(typepe[pp])
                    break
                else:
                    p=0
            if(p==0):
                label1.append(label[i])
                if isinstance(type[i],str):
                    type1.append([type[i]])
                else:
                    type1.append(type[i])
    return label1,type1#保存除去只有大小写差别之后的词条list，相对应的type

def _tiaocibold2(label,type,resource):#将只有大小写不同的剔除出去,并且合并type和resource
    x=len(label)
    label1=[]
    type1=[]#类型由['','','']变为[['',''],['']]
    resource1=[]
    for i in range(0,x):
        if(i==0):
            label1.append(label[i])
            if isinstance(type[i],str):
                type1.append([type[i]])
            else:
                type1.append(type[i])
            if isinstance(resource[i],str):
                resource1.append([resource[i]])
            else:
                resource1.append(resource[i])
        else:
            p=0
            for j in range(0,len(label1)):
                if(label1[j].lower()==label[i].lower()):
                    p=1
                    if isinstance(type[i],str):
                        type1[j].append(type[i])
                    else:
                        typepe=type[i]
                        for pp in range(0,len(typepe)):
                            type1[j].append(typepe[pp])
                    if isinstance(resource[i],str):
                        resource1[j].append(resource[i])
                    else:
                        resourcepe=resource[i]
                        for pp in range(0,len(resourcepe)):
                            resource1[j].append(resourcepe[pp])
                    break
                else:
                    p=0
            if(p==0):
                label1.append(label[i])
                if isinstance(type[i],str):
                    type1.append([type[i]])
                else:
                    type1.append(type[i])
                if isinstance(resource[i],str):
                    resource1.append([resource[i]])
                else:
                    resource1.append(resource[i])
    return label1,type1,resource1#保存除去只有大小写差别之后的词条list，相对应的type


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

def _tiaocisuo1(label,type):#将不用翻译的缩写提取出来，单独放在labelsuo，并且单独存放type
    x=len(label)
    label1=[]
    type1=[]
    labelsuo=[]
    typesuo=[]
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
                typesuo.append(type[i])
            else:
                label1.append(label[i])
                type1.append(type[i])
        else:
            label1.append(label[i])
            type1.append(type[i])
    return label1,type1,labelsuo,typesuo#分别存放去除缩写的词条，去除缩写的type，只有缩写的词条，只有缩写的type

def _tiaocisuo2(label,type,resource):#将不用翻译的缩写提取出来，单独放在labelsuo，并且单独存放type和resource
    x=len(label)
    label1=[]
    type1=[]
    resource1=[]
    labelsuo=[]
    typesuo=[]
    ressuo=[]
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
                typesuo.append(type[i])
                ressuo.append(resource[i])
            else:
                label1.append(label[i])
                type1.append(type[i])
                resource1.append(resource[i])
        else:
            label1.append(label[i])
            type1.append(type[i])
            resource1.append(resource[i])
    return label1,type1,resource1,labelsuo,typesuo,ressuo#分别存放去除缩写的词条，去除缩写的type和resource，只有缩写的词条，只有缩写的type和resource


def _tiaocitong(label):#查找可以由其他词条的翻译结果推断出来的词条，并给出对应词条index和本词条的对应位置（0，（2,15））#re.search函数太难使了，太多bug了
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
                if(len(line[j])<len(x)):
                    #print('1',x)
                    #print('2',line[j])
                    xp=line[j]
                    p=0
                    for ii in range(0,len(line[j])):
                        if(xp[ii]=='['):
                            p=1
                            break
                        if(xp[ii]=='+'and xp[ii-1]=='+'):
                            p=1
                            break
                    if(p==0): 
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
                    else:
                    # print('NONE')
                        _res.append('Y')
                else:
                    # print('NONE')
                        _res.append('Y')
                
        
    return _res

def _tiaocitong2(label):#自己写的是否可推断函数
    _res=[]
    _res.append('Y')
    for i in range(1,len(label)):
        x=label[i]
        for j in range(0,i):
            y=label[j]
            yn=0#对比词的index
            yl=0#对比词的长度
            beg=0#是否延续标志
            you=0#是否对应成功标志
            ye=0#设置end，如果这个end是0没有变，就说明没找到
            """if(len(y)>len(x)):
                break
            else:"""
            for p in range(0,len(x)):
                if(beg==1 and yl==len(y)):#相同截止
                    beg=0
                    ye=p-1
                    #print(3)
                    break
                if(beg==0 and x[p]==y[yn]):#启动
                    #print(1,p,x[p],y[yn])
                    beg=1
                    yl+=1
                    yn+=1
                    yb=p
                    continue   
                if(beg==1 and x[p]==y[yn]):#延续
                    #print(2,yn,x[p],y[yn])
                    beg=1
                    yl+=1
                    yn+=1
                    continue
                    
                if(beg==1 and x[p]!=y[yn]):#不同截止
                    #print(4,yn,x[p],y[yn])
                    beg=0
                    yl=0
                    yn=0 
                    continue
                        
                    
            if(yl==len(y) and ye!=0):
                you=1
                #print(x,'1',y)
                str=(j,(yb,ye)) 
                break
        if(you==1):
            _res.append(str)  
        else:
            _res.append('Y')

    return _res

def _xiangsi(x,y):#判断两个词的相似程度
    p=0
    for i in range(0,len(x)):

        for j in range(0,len(y)):

            if(x[i]==y[j]):
                p+=1
    if(p/len(y)>=2/3 and p/len(x)>=2/3):
        x=1
    else:
        x=0
    return x


def _tiaocixiangsi(label):#判断列表中的词条是不是十分相似，比如是否就是改了下顺序加个标点符号
    token=[]
    res0=[]
    restoken=[]
    
    for i in range(0,len(label)):
        token.append(nltk.word_tokenize(label[i]))
    for i in range(0,len(label)):
        if(i==0):
            res0.append(label[0])
            restoken.append(token[0])
            continue
        else:
            p=0
            for j in range(0,len(res0)):
                if(_xiangsi(token[i],restoken[j])==1):
                    p=1
                    break
            if(p==0):
                res0.append(label[i])
                restoken.append(token[i])
    return res0