import csv
import nltk
import http.client
import hashlib
from urllib import parse
import random
import time,re
import myfre
import tiaoci
import fanyibaidu
import os
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

def PNtran(file):
    #_path="/home/zjg/code2/file/Diseasr_or_Syndrome_All_AGGREGATED.tsv"
    #_path="/home/zjg/code2/file/test1.tsv"
    _path="/home/zjg/code2/file1/"+file
    [at,ad1,ad2,ad3]=getword(_path)
    #print(ad1[2],ad2[2],ad3[2])
    aPN=[]
    #仅提取标签为PN的词条
    for i in range(0,len(at)):
        aPN.append([])
        xad2=ad2[i]
        xad1=ad1[i]
        for j in range(0,len(xad2)):
            if(xad2[j]=='PN'):
                aPN[i].append(xad1[j])

    #保存标签为PN的词条
    with open('/home/zjg/code2/result1/PNen-'+file,'w',newline='')as f:
        for i in range(0,len(aPN)):
            af=aPN[i]
            f.write('%s\t%s\n' %(at[i],af))
    f.close()
    #翻译标签为PN的词条
    with open('/home/zjg/code2/result1/PNzh-'+file,'w',newline='')as f:
        ff=int(len(aPN)/800)#分成100份拼接翻译，提高速度
        for p in range(0,800):
            af1='' 
            if(p==799):
                ab=p*ff
                ae=len(aPN)
            else:
                ab=p*ff
                ae=(p+1)*ff
            for i in range(ab,ae):
                if(len(aPN[i])==0):
                    af1+='330\n'           #空词条以'330'代替，便于识别，避免翻译出错
                else:
                    aPNs=aPN[i]
                    for j in range(0,len(aPNs)):
                        af1+=aPNs[j]+'\n'
            #print(af1)  
            #调用百度API
            _len=ae-ab
            lines2=fanyibaidu.baidufanyi(af1,_len)

            #写入文件
            i=0
            i2=p*ff
            while(i<len(lines2)):
                if(lines2[i]=='330'):
                    k=[]
                    f.write('%s\t%s\n' %(at[i2],k))
                    i+=1
                    i2+=1
                else:
                    aPNs=aPN[i2]
                    """if(i2>140000):
                     print(i2)"""
                    af2=[]
                    for j in range(0,len(aPNs)):
                        #print(len(lines2),i+j)
                        """if(i+j==819):
                            print(ab,ae,ff,len(aPN))"""
                        af2.append(lines2[i+j])
                    f.write('%s\t%s\n' %(at[i2],af2))
                    i+=len(aPNs)
                    i2+=1
            

    f.close()

def get_filelist(dir):#依次遍历.json文件
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 
            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist

path ='/home/zjg/code2/file1/'


Filelist = get_filelist(dir)
print(Filelist)

for i in range(4,6):
    #2号没翻译完
    x=PNtran(Filelist[i])
    time.sleep(300)



#x=PNtran('Body_All_AGGREGATED.tsv')