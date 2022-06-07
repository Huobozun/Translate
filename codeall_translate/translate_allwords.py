

#本文件是翻译所有词条

import time
import fanyibaidu
import os
path = os.getcwd()


def _fretran(file):

    #提取翻译词条文件的title和词条
    with open(path+'/needtran-words/'+file,'r',encoding='utf-8')as fr:
        dataci=[]
        for line in fr:
            dataci.append(line)
        fr.close()
    z=[]
    t=[]
    for ii in range(0,len(dataci)):
        x=dataci[ii]
        yy=''
        for i in range(0,len(x)):
            yy+=x[i]
        z.append(eval(yy))

    awords=z



    #翻译词条
    with open(path+'/aftertran-words/'+file,'w',newline='')as f:
        ix=0
        while(ix<len(awords)):
            time.sleep(0.2)
            iy=0
            il=0
            af1='' 
            while(iy<400 and ix+iy<len(awords) and len(af1)<4500):
                if(len(awords[ix+iy])==0):
                    il+=1
                    af1+='330\n'           #空词条以'330'代替，便于识别，避免翻译出错
                else:
                    awordsall=awords[ix+iy]
                    for j in range(0,len(awordsall)):
                        il+=1
                        af1+=awordsall[j]+'\n'
                iy+=1
                
            lines2=fanyibaidu.baidufanyi(af1,il)

            i=0
            i2=ix
            while(i<len(lines2)):
                if(lines2[i]=='330'):
                    k=[]
                    f.write('%s\n' %(k))
                    i+=1
                    i2+=1
                else:
                    awordsall=awords[i2]
                    af2=[]
                    for j in range(0,len(awordsall)):
                        af2.append(lines2[i+j])
                    f.write('%s\n' %(af2))
                    i+=len(awordsall)
                    i2+=1
            ix+=iy
            

    f.close()



if __name__ == "__main__":

    path1 =path+'/needtran-words/'
    Filelist = os.listdir(path1)
    print(Filelist)

    for i in range(0,len(Filelist)):
        print(Filelist[i])
        x=_fretran(Filelist[i])
        time.sleep(5)
