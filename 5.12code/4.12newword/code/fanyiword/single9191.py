
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
        fy=get_content('filenew\\',Filelist[i])#list里类型为list
        fw=get_content('result-fanyi\\','zh2-'+Filelist[i])#list里类型为list
        for i in range(0,len(ftitle)):
            fw1=fw[i]
            fy1=fy[i]
            if(i==9191): 
                x=[]
                jx=0
                print(fy1[7994])
                lines2=fanyibaidu.baidufanyi(fy1[7994],1)
                print(lines2)
                print(fy1[7995])
                lines2=fanyibaidu.baidufanyi(fy1[7995],1)
                print(lines2)
                #print(len(fy1))7996
                """while(jx<7995):
                    fan=''
                    jx2=0
                    while(jx+jx2<7995 and len(fan)<5000):
                        fan+=fy1[jx+jx2]+'\n'
                        jx2+=1
                    print(jx,jx2,jx+jx2)
                    #time.sleep(1)
                    lines2=fanyibaidu.baidufanyi(fan,jx2)
                    #print(lines2)
                    for jy in range(0,len(lines2)):
                        x.append(lines2[jy])
                    jx+=jx2
                with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\result-fanyi\\signle",'w',encoding='utf-8')as fa:
                    fa.write('%s\t%s\n' %(ftitle[i],x))
                    fa.close()"""
                #print(fy1)
                #print(x)
                


 

