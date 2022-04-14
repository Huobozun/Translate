
#将空词条的第一个词翻译之后，统计标记已经翻译过的词

import os 
import json
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
    for i in range(0,len(Filelist)):

        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        fl=get_content('resultall2/Mark_word1/M10-',Filelist[i])
        fm=get_index('resultall2/mark_index_PNMSHfre/mPNMSHfre-',Filelist[i])#list里类型为list
        with open('/home/zjg/code2/resultall3.2/mark_index_PNMSHfre11/mPNMSHfre11-'+Filelist[i],'w',newline='')as fa:
            for i1 in range(0,len(fm)):
                fm1=fm[i1]
                fl1=fl[i1]
                if(fl1[0]==0):#第一个词条没翻译
                    x=[0]
                    for i2 in range(0,len(fm1)):
                        x.append(fm1[i2])
                    fa.write('%s\t%s\n' %(ftitle[i1],x))
                else:#第一个词条翻译了
                     fa.write('%s\t%s\n' %(ftitle[i1],fm1))
            fa.close()








 