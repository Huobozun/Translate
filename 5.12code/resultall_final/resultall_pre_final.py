

#本版本是将所有的翻译结果转化成对应展示形式

import csv
import nltk
import http.client
import hashlib
from urllib import parse
import random
import time,re
import os


def get_content(name,file):
    with open('/home/zjg/code2/'+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(9,len(x)):
                y+=x[i]
            z.append(eval(y))
    return z

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
                if(b==3 and j==len(line0)-1):
                    word+=line0[j]
                    data3[i].append(word)
                    j=len(line0)
                    b=1
                    word=''
                    continue
                else:
                    word+=line0[j]  
                    j+=1 
    f.close()
    return title,data1,data2,data3 #title是每行的title的list,对应的，data1是每行的英文单词的集合的list,data2是term type，data3是出处


def get_filelist(dir):#依次遍历.json文件
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 

            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist


if __name__ == "__main__":
    path ='/home/zjg/code2/file/'

    Filelist = get_filelist(dir)
    print(Filelist)
    for i1 in range(0,len(Filelist)):
        file=Filelist[i1]
        _path="/home/zjg/code2/resultall6.0/"+file
        [at,ad1,ad2,ad3]=getword(_path)
        with open('/home/zjg/code2/resultall_final/zh-'+file,'w',encoding='utf-8',newline='')as fw:
            fl=get_content('resultall6.0/Mark_index6.0/M-',file)#list里类型为list
            for i2 in range(0,len(fl)):
                fl1=fl[i2]
                ad11=ad1[i2]
                ad22=ad2[i2]
                ad33=ad3[i2]
                fw.write('%s\t' %(at[i2]))
                fword=''
                for i3 in range(0,len(fl1)):
                    if(i3!=0):
                        fword=fword+' [SEP] '

                    for i4 in range(0,len(fl1)):
                        if(fl1[i4]==i3):
                            break
                    
                    fword=fword+ad11[i4]+'###'+ad22[i4]+'###'+ad33[i4]
                fw.write('%s\n' %(fword))
        fw.close()
                


