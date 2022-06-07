
#统计一下还需要翻译的词条数量

import os 
import json
import sys
import time
sys.path.append('/home/zjg/code2/')
import fanyibaidu
def get_title(name,file):
    with open('/home/zjg/code2/'+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close()
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(0,8):
                y+=x[i]
            z.append(y)
    return z


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

def get_index(name,file):
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

def get_word(name,file):
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

    path ='/home/zjg/code2/result-word/'
    Filelist = get_filelist(dir)
    with open('/home/zjg/code2/resultall5.0/ALLcount.tsv','w',newline='')as fa:
        y=0
        y0=0
        for i in range(0,len(Filelist)):

            fl=get_content('resultall4.0/Mark_word4.0/M-',Filelist[i])#list里类型为list
            x=0
            x0=0
            for i1 in range(0,len(fl)):
                fl1=fl[i1]
                for i2 in range(0,len(fl1)):
                    x0+=1
                    if(fl1[i2]==0):
                        x+=1
            fa.write('%s\t%s\t%s\n' %(Filelist[i],x,x0))
            y+=x
            y0+=x0
        fa.write('total:\t%s\t%s\n' %(y,y0))
        fa.close()
     








 