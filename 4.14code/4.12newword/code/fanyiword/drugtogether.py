
#没有第一个词条的翻译结果，边判断是否为空边翻译

import os 
import json
import sys
import time
sys.path.append("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword")
import fanyibaidu
def get_title(name,file):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\"+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(0,7):
                y+=x[i]
            z.append(y)
    return z


def get_content(name,file):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\"+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(8,len(x)):
                y+=x[i]
            #print(ii)
            z.append(eval(y))
    return z

def get_index(name,file):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\"+name+file,'r',encoding='utf-8')as ft:
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

def get_word(name,file):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\"+name+file,'r',encoding='utf-8')as ft:
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
            z.append(y)
    return z

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
    Filelist=['drug.tsv']
    for i in range(0,len(Filelist)):

        ftitle=get_title('result-fanyi\\','zh-'+Filelist[i])#list里类型为str
        f2=get_content('result-fanyi\\','signle')#list里类型为list
        f1=get_content('result-fanyi\\','zh2-'+Filelist[i])#list里类型为list
        with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\result2-fanyi\\All-drug.tsv",'w',encoding='utf-8',newline='')as fr:
            for i in range(0,len(ftitle)):
                if(i==9191):
                    fr.write('%s\t%s\n' %(ftitle[i],f2[0]))
                else:
                    fr.write('%s\t%s\n' %(ftitle[i],f1[i]))
