
#将所有剩下没有翻译的词进行翻译

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


def fanyiall(filename,begin):
        print(filename)
        ftitle=get_title('/result-type/',filename)#list里类型为str
        ft=get_content('/result-type/',filename)#list里类型为list
        fr=get_content('/result-resouce/',filename)#list里类型为list
        fw=get_content('/result-word/',filename)#list里类型为list
        fl=get_content('/Mark_word4.0/M-',filename)#list里类型为list
        with open(basepath+'/Add-'+filename,'a',newline='')as fa:
            ix=begin
            while(ix<len(fw)):
            #while(ix<20000):
                #print(ix)
                time.sleep(0.2)
                iy=0
                il=0
                af1='' 
                while(iy<700 and ix+iy<len(fw) and len(af1)<4000):
                    xi9=0
                    fl1=fl[ix+iy]
                    for i9 in range(0,len(fl[ix+iy])):
                        if(fl1[i9]==0):
                            
                            il+=1
                            af1+=fw[ix+iy][i9]+'\n'#抽出第一个词进行翻译
                        else:
                            xi9+=1
                    if(xi9==len(fl1)):
                        il+=1
                        af1+='330\n'           #空词条以'330'代替，便于识别，避免翻译出错
                    iy+=1
                    
                lines2=fanyibaidu.baidufanyi(af1,il)
                #print(lines2)
                i=0
                i2=ix
                while(i<len(lines2)):
                    if(lines2[i]=='330'):
                        k=[]
                        fa.write('%s\t%s\n' %(ftitle[i2],k))
                        i+=1
                        i2+=1
                    else:
                        fls=fl[i2]
                        af2=[]
                        ic=0
                        for j in range(0,len(fls)):
                            if(fls[j]==0):
                                #print(len(lines2),i,i+j)
                                af2.append(lines2[i])
                                i+=1
                        fa.write('%s\t%s\n' %(ftitle[i2],af2))
                        #print(af2)
                        i2+=1
                rbegin=i2
                ix+=iy
                

            fa.close()
        return rbegin

def try_fanyi(filename,begin):
    try:
        x1=fanyiall(filename,begin)
    except KeyError:
        try:
            print('ERROR 1')
            time.sleep(5)
            x2=fanyiall(filename,x1)
        except KeyError:
            try:
                print('ERROR 2')
                time.sleep(5)
                x3=fanyiall(filename,x2)
            except KeyError:
                print('ERROR 3')
                time.sleep(5)
                x4=fanyiall(filename,x3)

if __name__ == "__main__":

    path =basepath+'/result-word/'
    Filelist = get_filelist(dir) 
    print(Filelist)
    
    #x1=try_fanyi(Filelist[1],3257)

    #x2=try_fanyi(Filelist[0],0)
    
    #time.sleep(5)
    #for i in range(13,len(Filelist)):
    
    x=try_fanyi(Filelist[15],10020)
    time.sleep(5)
        








 