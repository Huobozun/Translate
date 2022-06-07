

#本文件是挑选出十年内出现频率大于10的词条并进行翻译
import time
import fanyibaidu
import os
path = os.getcwd()




def _fretran(file):

    #提取翻译词条文件的title和词条
    with open(path+'/resultfre2-10years/Hfre-'+file,'r',encoding='utf-8')as fr:
        dataci=[]
        for line in fr:
            dataci.append(line)
        fr.close()
    z=[]
    t=[]
    for ii in range(0,len(dataci)):
        x=dataci[ii]
        y=''
        yy=''
        for i in range(0,8):
            y+=x[i]
        t.append(y)
        for i in range(9,len(x)):
            yy+=x[i]
        z.append(eval(yy))

    awords=z
    at=t


    #翻译频率高的词条
    with open(path+'/resultfre2-10years/resultfre&baidu/Hfre-zh-'+file,'w',newline='')as f:
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
                    awordss=awords[ix+iy]
                    for j in range(0,len(awordss)):
                        il+=1
                        af1+=awordss[j]+'\n'
                iy+=1
                
            lines2=fanyibaidu.baidufanyi(af1,il)

            i=0
            i2=ix
            while(i<len(lines2)):
                if(lines2[i]=='330'):
                    k=[]
                    f.write('%s\t%s\n' %(at[i2],k))
                    i+=1
                    i2+=1
                else:
                    awordss=awords[i2]
                    af2=[]
                    for j in range(0,len(awordss)):
                        #print(len(lines2),i+j)
                        af2.append(lines2[i+j])
                    f.write('%s\t%s\n' %(at[i2],af2))
                    i+=len(awordss)
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
        time.sleep(10)
