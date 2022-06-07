
#标记所有剩下的需要翻译的词的index

import os 
basepath = os.path.dirname(__file__)
import json
import sys
import time
sys.path.append('/home/zjg/code2/')
import fanyibaidu
def get_title(name,file):
    with open(basepath+name+file,'r',encoding='utf-8')as ft:
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
    with open(basepath+name+file,'r',encoding='utf-8')as ft:
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
    with open(basepath+name+file,'r',encoding='utf-8')as ft:
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
    with open(basepath+name+file,'r',encoding='utf-8')as ft:
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


def markall(filename):
        print(filename)
        ftitle=get_title('/result-type/',filename)#list里类型为str
        ft=get_content('/result-type/',filename)#list里类型为list
        fr=get_content('/result-resouce/',filename)#list里类型为list
        fw=get_content('/result-word/',filename)#list里类型为list
        fl=get_content('/Mark_word4.0/M-',filename)#list里类型为list
        with open(basepath+'/mark_index5/M-'+filename,'w',newline='')as fa:
            
            for i1 in range(0,len(fl)):
                fl1=fl[i1]
                x=[]
                for i2 in range(0,len(fl1)):
                    if(fl1[i2]==0):
                        x.append(i2)

                fa.write('%s\t%s\n' %(ftitle[i1],x))

            fa.close()



if __name__ == "__main__":

    path =basepath+'/result-word/'
    Filelist = get_filelist(dir) 
    print(Filelist)
    
    #x1=try_fanyi(Filelist[1],3257)

    #x2=try_fanyi(Filelist[0],0)
    
    #time.sleep(5)
    for i in range(0,len(Filelist)):
    
        x=markall(Filelist[i])
        








 