import csv
import nltk
import http.client
import hashlib
from urllib import parse
import random
import time,re
import myfre
import tiaoci
def getword(path):
    with open(path, 'r', encoding='utf-8') as f:
        data=[]
        title=[]
        for line in f:
                # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
                line = line.strip('\n').split('\t')  
                #print(line[0])
                #print(line[1])
                #print(line[2])
                #break
                data.append(line[1])
                title.append(line[0])
        #print(data[0])#此时data中的每个元素就是每行的第二列
        #抽出每行的单词
        data1=[]#将每行单词都排起来
        data2=[]#type
        data3=[]#出处
        for i in range(0,len(data)):
            line0=data[i]
            data1.append([])
            data2.append([])
            data3.append([])
            word=''
            j=0
            b=1
            while(j<len(line0)):
                if(b==1 and line0[j]=='#'and line0[j+1]=='#'and line0[j+2]=='#'):
                    data1[i].append(word)
                    j+=3
                    b=2
                    word=''
                    continue
                if(b==2 and line0[j]=='#'and line0[j+1]=='#'and line0[j+2]=='#'):
                    data2[i].append(word)
                    j+=3
                    b=3
                    word=''
                    continue
                if(b==3 and line0[j]==' 'and line0[j+1]=='['and line0[j+2]=='S'and line0[j+3]=='E'and line0[j+4]=='P'and line0[j+5]==']'and line0[j+6]==' '):
                    data3[i].append(word)
                    j+=7
                    b=1
                    word=''
                    continue
                if(b==3 and line0[j]=='\t'):
                    data2[i].append(word)
                    j=len(line0)
                    b=1
                    word=''
                    continue
                else:
                    word+=line0[j]  
                    j+=1 
    return title,data1,data2,data3 #title是每行的title的list,对应的，data1是每行的英文单词的集合的list,data2是term type，data3是出处


"""_path="/home/zjg/code2/file/Diseasr_or_Syndrome_All_AGGREGATED.tsv"
#_path="/home/zjg/code2/file/test1.tsv"
[at,ad0,ad2,ad3]=getword(_path)
#print(a)

#求数量
num=0
for i in range(0,len(ad0)):
    b=ad0[i]
    for j in range(0,len(b)):
        c=b[j]
        num+=len(c)
print('原始数量:',num)

#1111111111去除重复的
ad1=[]
for i in range(0,len(ad0)):
    ad1.append(tiaoci._tiaocichongfu(ad0[i]))

#求去除重复后的数量
num1=0
for i in range(0,len(ad1)):
    b=ad1[i]
    for j in range(0,len(b)):
        c=b[j]
        num1+=len(c)
print('1去重复:',num1)

#2222222222222去除大小写差异
ad2=[]
for i in range(0,len(ad0)):
    ad2.append(tiaoci._tiaocibold(ad0[i]))

#求去除大小差异后的数量
num2=0
for i in range(0,len(ad2)):
    b=ad2[i]
    for j in range(0,len(b)):
        c=b[j]
        num2+=len(c)
print('2去大小写:',num2)

#3.5 3.5 3.5 3.5去除复数
ad3=[]
for i in range(0,len(ad2)):
    ad3.append(tiaoci._tiaociss(ad2[i]))

#求去除复数后的数量
num3=0
for i in range(0,len(ad3)):
    b=ad3[i]
    for j in range(0,len(b)):
        c=b[j]
        num3+=len(c)
print('3.5去复数:',num3)

#44444444去除缩写词条，并将缩写词条放入adsuo
ad4=[]
adsuo=[]
for i in range(0,len(ad3)):
    x=''
    y='' 
    [x,y]=tiaoci._tiaocisuo(ad3[i])
    
    adsuo.append(y)
    ad4.append(x)

#求去除缩写词条后的数量
num4=0
for i in range(0,len(ad4)):
    b=ad4[i]
    for j in range(0,len(b)):
        c=b[j]
        num4+=len(c)
print('4去缩写:',num4)

""""""#555555555得到是否可以由其他词条推断本词条的判断表，并将判断表放到ad5b中
ad5b=[]
for i in range(0,len(ad4)):
    #print(ad4[i])   
    ad5b.append(tiaoci._tiaocitong2(ad4[i]))
#print(ad5b)
#不翻译求数量
num5=0
for i in range(0,len(ad5b)):
    b=ad4[i]
    c=ad5b[i]
    for j in range(0,len(b)):
        if(c[j]=='Y'):
            num5+=len(b[j])
    
print('5不翻译:',num5)
#少翻译求数量
num55=0
for i in range(0,len(ad5b)):
    b=ad4[i]
    c=ad5b[i]
    for j in range(0,len(b)):
        if(c[j]=='Y'):
            num55+=len(b[j])
        else:
            xx=c[j]
            x=xx[1]
            num55+=len(b[j])-(x[1]-x[0]+1)
    
print('5少翻译:',num55)"""
"""
#666666相似的词不翻译，比如已经翻译了'Adenofibroma NOS'，就不再翻译'NOS，Adenofibroma'
ad6=[]
for i in range(0,len(ad4)):
    #print(ad4[i])   
    ad6.append(tiaoci._tiaocixiangsi(ad4[i]))
#print(ad5b)
#去相似求数量
num6=0
for i in range(0,len(ad6)):
    b=ad6[i]
    for j in range(0,len(b)):
        c=b[j]
        num6+=len(c)
print('6去相似:',num6)
"""

"""with open('tici.tsv','w',newline='')as f:
    for i in range(0,len(ad4)):
        af=ad4[i]
        f.write('%s\t%s\n' %(at[i],af))
f.close()"""

"""text='abdomen neoplasm abdomen tumors abdomen tumours Abdomen -- Tumors Abdominal abdomen neoplasm neoplasm NOS'
b=myfre._myfreq(text,['abdomen','neoplasm','abdomen neoplasm'])
print(b)
"""
