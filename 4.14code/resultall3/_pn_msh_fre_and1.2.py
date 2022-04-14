
#没有第一个词条的翻译结果，边判断是否为空边翻译

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
    for i in range(1,len(Filelist)):

        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        ft=get_content('result-type/',Filelist[i])#list里类型为list
        fr=get_content('result-resouce/',Filelist[i])#list里类型为list
        fw=get_content('result-word/',Filelist[i])#list里类型为list
        fword=get_word('resultall2/',Filelist[i])#list里类型为str
        with open('/home/zjg/code2/resultall3/3-'+Filelist[i],'w',newline='')as fa:
            i1=0
            while(i1<len(ft)):
                fword1=fword[i1]
                fword1=fword1.replace('\n','')
                fanyiw=''
                i2=0
                while(len(fword1)==0 and i1+i2<len(ft) and len(fanyiw)<3000):
                    fanyiw+=fw[i1+i2][0]+'\n'
                    i2+=1
                    if(i1+i2<len(ft)):
                        fword1=fword[i1+i2]
                        fword1=fword1.replace('\n','')

                if(i2>0):
                    resfanyiw=fanyibaidu.baidufanyi(fanyiw,i2-1)
                    i3=0
                    while(i3<i2):
                        fresfanyiw=resfanyiw[i3]+'###'+ft[i1+i3][0]+'###'+fr[i1+i3][0]
                        fa.write('%s\t%s\n' %(ftitle[i1+i3],fresfanyiw))#重新写进新的文件
                        i3+=1
                    i1+=i2
                else:
                    
                    fa.write('%s\t%s\n' %(ftitle[i1],fword1))#重新写进新的文件
                    i1+=1

                

            fa.close()
        time.sleep(5)








 