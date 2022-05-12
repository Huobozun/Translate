
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
        fw=get_content('result-fanyi\\','zh-'+Filelist[i])#list里类型为list
        with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\result-fanyi\\zh2-"+Filelist[i],'a',encoding='utf-8',newline='')as fa:
            for i in range(9192,len(ftitle)):
                fw1=fw[i]
                fy1=fy[i]
                fr=[]
                j1=0
                if(fw1[0]=='错啦'):
                    fan=''
                    for j3 in range(0,len(fy1)):
                        fan+=fy1[j3]+'\n'
                    lines2=fanyibaidu.baidufanyi(fan,len(fy1))
                    for j4 in range(0,len(lines2)):
                        fr.append(lines2[j4])
                    fa.write('%s\t%s\n' %(ftitle[i],fr))
                    continue
                while(j1<len(fw1)):
                    j2=0
                    fan=''
                    #print(fw1[j1])
                    if(fw1[j1]!='翻译出错' and fw1[j1]!='1翻译出错'):
                        fr.append(fw1[j1])
                        j1+=1
                    else:
                        while(j1+j2<len(fw1) and len(fan)<4000 and (fw1[j1+j2]=='翻译出错' or fw1[j1+j2]=='1翻译出错')):
                                print(fy1[j1+j2],11,fw1[j1+j2],'\n')
                                fan+=fy1[j1+j2]+'\n'
                                j2+=1
                        j1+=j2
                        lines2=fanyibaidu.baidufanyi(fan,j2)
                        for jj in range(0,len(lines2)):
                            fr.append(lines2[jj])
                fa.write('%s\t%s\n' %(ftitle[i],fr))
            fa.close()

                            





 