

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
    #_path="/home/zjg/code2/file/Diseasr_or_Syndrome_All_AGGREGATED.tsv"
    
   
    #读取词条
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\file2\\"+file,'r',encoding='utf-8')as f:
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
    #print(len(aPN[112]))

    #翻译词条
    with open('D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\result-fanyi\\zh-'+file,'a',encoding='utf-8',newline='')as f:
        ix=9192
        while(ix<len(aPN)):
        #while(ix<20000):
            #print(ix)
            time.sleep(0.2)
            iy=0
            il=0
            af1='' 
            while(iy<500 and ix+iy<len(aPN) and len(af1)<2000):
                if(len(aPN[ix+iy])==0):
                    il+=1
                    af1+='330\n'           #空词条以'330'代替，便于识别，避免翻译出错
                else:
                    aPNs=aPN[ix+iy]
                    for j in range(0,len(aPNs)):
                        il+=1
                        af1+=aPNs[j]+'\n'
                iy+=1
                
            lines2=fanyibaidu.baidufanyi(af1,il)

            i=0
            i2=ix
            while(i<len(lines2)):
                if(lines2[i]=='330'):
                    k=[]
                    f.write('%s\t%s\n' %(at[i2],k))
                    i+=1
                    i2+=1
                else:
                    aPNs=aPN[i2]
                    af2=[]
                    for j in range(0,len(aPNs)):

                        #if(i2==112 and i+j==444):
                            #print(aPNs[444],111,aPNs[443],lines2[443])
                        #print(i2,il,len(lines2),i+j)
                        if(i+j<len(lines2)):
                            af2.append(lines2[i+j])
                        else:
                            af2.append('1翻译出错')
                    f.write('%s\t%s\n' %(at[i2],af2))
                    i+=len(aPNs)
                    i2+=1
            ix+=iy
            

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

    """for i in range(5,len(Filelist)):
        #drug.tsv   pharmcube.tsv
        x=PNtran(Filelist[i])
        time.sleep(10)"""

    
    x=PNtran('drug.tsv')