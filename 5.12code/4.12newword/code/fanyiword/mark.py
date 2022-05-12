

#本版本是根据合成文件数量以及限制字符长度进行翻译MSH

import csv
import http.client
import hashlib
from urllib import parse
import random
import time,re
import fanyibaidu
import os

def PNtran(file):
   
    
    #读取词条
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\filenew\\"+file,'r',encoding='utf-8')as f:
        data=[]
        title=[]
        for line in f:
                # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
                line = line.strip('\n').split('\t')  
                #print(line[0])
                #print(line[1])
                #print(line[2])
                #break
                data.append(eval(line[1]))
                title.append(line[0])
    f.close()
    at=title
    aPN=data
    #标注翻译词条
    with open('D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\mark-newword\\MN-'+file,'w',encoding='utf-8')as f:
        for i in range(0,len(at)):
            aPNs=aPN[i]
            x=[]
            for j in range(0,len(aPNs)):
                x.append(1)
            f.write('%s\t%s\n' %(at[i],x))

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


if __name__ == "__main__":
    path ="D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\filenew"

    Filelist = get_filelist(dir)
    print(Filelist)

    for i in range(0,len(Filelist)):
        #drug   pharmcube
        x=PNtran(Filelist[i])
        time.sleep(10)

    
    #x=PNtran('Organic_Chemical_All_AGGREGATED.tsv')