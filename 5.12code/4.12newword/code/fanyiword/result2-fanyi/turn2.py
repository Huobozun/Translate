
#没有第一个词条的翻译结果，边判断是否为空边翻译

import os 
import json
import sys
import time

from pytest import File
sys.path.append("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword")
import fanyibaidu
def get_title(name,file,xx):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\"+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            if(dataci[ii][xx]!='	'):
                x=dataci[ii]
                y=''
                for i in range(0,10):
                    y+=x[i]
            else:
                x=dataci[ii]
                y=''
                for i in range(0,xx):
                    y+=x[i]
            z.append(y)
    return z


def get_content(name,file,xx):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\"+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            if(dataci[ii][xx]!='	'):
                x=dataci[ii]
                y=''
                for i in range(11,len(x)):
                    y+=x[i]
            else:
                x=dataci[ii]
                y=''
                for i in range(xx+1,len(x)):
                    y+=x[i]
            print(ii)
            z.append(eval(y))
    return z

def get_index(name,file):
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\"+name+file,'r',encoding='utf-8')as ft:
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

    path ="D:\\ZJG\\zjg2\\4.12newword\\code\\newfile2\\word"
    Filelist = get_filelist(dir)
    print(Filelist)
    file='target_polypeptide.tsv'
    ftitle=get_title('result2-fanyi\\2\\','All-'+file,6)#list里类型为str
    fw=get_content('result2-fanyi\\2\\','All-'+file,6)#list里类型为list
    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\result2-fanyi\\2turn\\"+file,'w',encoding='utf-8',newline='')as fr:
        for i in range(0,len(ftitle)):
            x=''
            fw1=fw[i]
            for j in range(0,len(fw1)):
                x+=fw1[j]
                if(j!=len(fw1)-1):
                    x+=' [SEP] '
            fr.write('%s\t%s\n' %(ftitle[i],x))
