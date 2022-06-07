
#已有翻译结果，将所有的翻译结果合起来

import os 
import json
import sys
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
    for i in range(0,len(Filelist)):

        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        ft=get_content('result-type/',Filelist[i])#list里类型为list
        fr=get_content('result-resouce/',Filelist[i])#list里类型为list
        fw=get_content('resultall5.0/Add-',Filelist[i])#list里类型为list
        fword=get_word('resultall4.0/',Filelist[i])#list里类型为str
        fm=get_content('resultall4.0/mark_index_PNMSHFRE112/mPNMSHFRE112-',Filelist[i])
        fmm=get_content('resultall5.0/mark_index5/M-',Filelist[i])
        with open('/home/zjg/code2/resultall6.0/'+Filelist[i],'w',newline='')as fa:
            with open('/home/zjg/code2/resultall6.0/Mark_index6.0/M-'+Filelist[i],'w',newline='')as fb:
                    for i1 in range(0,len(ft)):
                        ft1=ft[i1]
                        fr1=fr[i1]
                        fw1=fw[i1]
                        fm1=fm[i1]
                        fmm1=fmm[i1]
                        fword1=fword[i1]
                        fword1=fword1.replace('\n','')
                        for i2 in range(0,len(fw1)): 
                            fword1=fword1+' [SEP] '+fw1[i2]+'###'+ft1[int(fmm1[i2])]+'###'+fr1[int(fmm1[i2])]
                            fm1.append(int(fmm1[i2]))
                    
                        fa.write('%s\t%s\n' %(ftitle[i1],fword1))
                        fb.write('%s\t%s\n' %(ftitle[i1],fm1))
                        
                    fa.close()
                    fb.close()








 