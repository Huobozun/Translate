

#本版本是翻译十年内频率高的词条

import csv
import nltk
import http.client
import hashlib
from urllib import parse
import random
import time,re
import sys
sys.path.append("/home/zjg/code2")
import fanyibaidu
import os


def _fretran(file):

    #提取翻译词条文件的title和词条
    with open('/home/zjg/code2/resultfre2-10years/Hfre-'+file,'r',encoding='utf-8')as fr:
        dataci=[]
        for line in fr:
            dataci.append(line)
        fr.close()
    z=[]
    t=[]
    for ii in range(0,len(dataci)):
        x=dataci[ii]
        y=''
        yy=''
        for i in range(0,8):
            y+=x[i]
        t.append(y)
        for i in range(9,len(x)):
            yy+=x[i]
        z.append(eval(yy))

    aPN=z
    at=t


    #翻译频率高的词条
    with open('/home/zjg/code2/resultfre2-10years/resultfre&baidu/Hfre-zh-'+file,'w',newline='')as f:
        ix=0
        while(ix<len(aPN)):
        #while(ix<20000):
            #print(ix)
            time.sleep(0.2)
            iy=0
            il=0
            af1='' 
            while(iy<400 and ix+iy<len(aPN) and len(af1)<4500):
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
                        #print(len(lines2),i+j)
                        af2.append(lines2[i+j])
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
    path ='/home/zjg/code2/result-word/'
    Filelist = get_filelist(dir)
    print(Filelist)

    for i in range(0,len(Filelist)):
        print(Filelist[i])
        x=_fretran(Filelist[i])
        time.sleep(10)

    """['Cell_or_Molecular_Dysfunction_AGGREGATED.tsv', 'Pharmacologic_Substance_all_AGGREGATED.tsv', 'Organic_Chemical_All_AGGREGATED.tsv', 'Laboratory_or_Test_Result_AGGREGATED.tsv', 'Virus_AGGREGATED.tsv', 'Gene_or_Genome_AGGREGATED.tsv', 'test1.tsv', 'Clinical_Attribute_AGGREGATED.tsv', 'Pathologic_Function_AGGREGATED.tsv', 'Therapeutic_or_Preventive_Procedure_AGGREGATED.tsv', 'Indicator_Reagent_or_Diagnostic_Aid_AGGREGATED.tsv', 'Cell_all_AGGREGATED.tsv', 'Sign_or_Sympton_Aggregated.tsv', 'pharmcube.tsv']"""

    #x=PNtran('Organic_Chemical_All_AGGREGATED.tsv')