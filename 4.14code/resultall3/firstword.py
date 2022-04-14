
#将所有词条的第一个词进行翻译

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
    for i in range(11,len(Filelist)):

        #print(Filelist[i])
        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        ft=get_content('result-type/',Filelist[i])#list里类型为list
        fr=get_content('result-resouce/',Filelist[i])#list里类型为list
        fw=get_content('result-word/',Filelist[i])#list里类型为list
        fword=get_word('resultall2/',Filelist[i])#list里类型为str
        with open('/home/zjg/code2/resultall3/firstword/first-'+Filelist[i],'w',newline='')as fa:
            ix=0
            while(ix<len(fw)):
            #while(ix<20000):
                #print(ix)
                time.sleep(0.2)
                iy=0
                il=0
                af1='' 
                while(iy<1000 and ix+iy<len(fw) and len(af1)<4000):
                    if(len(fw[ix+iy])==0):
                        il+=1
                        af1+='330\n'           #空词条以'330'代替，便于识别，避免翻译出错
                    else:  
                        il+=1
                        af1+=fw[ix+iy][0]+'\n'#抽出第一个词进行翻译
                    iy+=1
                    
                lines2=fanyibaidu.baidufanyi(af1,il)

                i=0
                i2=ix
                while(i<len(lines2)):
                    if(lines2[i]=='330'):
                        k=[]
                        fa.write('%s\t%s\n' %(ftitle[i2],k))
                        i+=1
                        i2+=1
                    else:
                        af2=[]
                        af2.append(lines2[i])
                        fa.write('%s\t%s\n' %(ftitle[i2],af2))
                        i+=1
                        i2+=1
                ix+=iy
                

            fa.close()
        time.sleep(5)








 