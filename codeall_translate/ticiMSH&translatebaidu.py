

#本版本是根据合成文件数量以及限制字符长度进行翻译MSH


import time
import fanyibaidu
import fanyibaidu
import os
path = os.getcwd()
def getword(path0):
    with open(path0, 'r', encoding='utf-8') as f:
        data=[]
        title=[]
        for line in f:
                # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
                line = line.strip('\n').split('\t')  

                data.append(line[1])
                title.append(line[0])
        #此时data中的每个元素就是每行的第二列
        #抽出每行的单词
        data1=[]#将每行单词都排起来
        data2=[]#type
        data3=[]#出处
        for i in range(0,len(data)):
            line0=data[i]
            data1.append([])
            data2.append([])
            data3.append([])
            word=''
            j=0
            b=1
            while(j<len(line0)):
                if(b==1 and line0[j]=='#'and line0[j+1]=='#'and line0[j+2]=='#'):
                    data1[i].append(word)
                    j+=3
                    b=2
                    word=''
                    continue
                if(b==2 and line0[j]=='#'and line0[j+1]=='#'and line0[j+2]=='#'):
                    data2[i].append(word)
                    j+=3
                    b=3
                    word=''
                    continue
                if(b==3 and line0[j]==' 'and line0[j+1]=='['and line0[j+2]=='S'and line0[j+3]=='E'and line0[j+4]=='P'and line0[j+5]==']'and line0[j+6]==' '):
                    data3[i].append(word)
                    j+=7
                    b=1
                    word=''
                    continue
                if(b==3 and j==len(line0)-1):
                    word+=line0[j]
                    data3[i].append(word)
                    j=len(line0)
                    b=1
                    word=''
                    continue
                else:
                    word+=line0[j]  
                    j+=1 
    return title,data1,data2,data3 #title是每行的title的list,对应的，data1是每行的英文单词的集合的list,data2是term type，data3是出处

def MSHtran(file):

    _path=path+"/file/"+file
    [at,ad1,ad2,ad3]=getword(_path)
    awords=[]
    #仅提取来源为MSH的词条
    for i in range(0,len(at)):
        awords.append([])
        xad3=ad3[i]
        xad1=ad1[i]
        for j in range(0,len(xad3)):
            if(xad3[j]=='MSH'):
                awords[i].append(xad1[j])

    #保存标签为MSH的词条
    with open(path+'/resultMSH/MSHen-'+file,'w',newline='')as f:
        for i in range(0,len(awords)):
            af=awords[i]
            f.write('%s\t%s\n' %(at[i],af))
    f.close()
    #翻译标签为MSH的词条
    with open(path+'/resultMSH/MSHzh-'+file,'w',newline='')as f:
        ix=0
        while(ix<len(awords)):
            time.sleep(0.2)
            iy=0
            il=0
            af1='' 
            while(iy<500 and ix+iy<len(awords) and len(af1)<5000):
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
                        af2.append(lines2[i+j])
                    f.write('%s\t%s\n' %(at[i2],af2))
                    i+=len(awordss)
                    i2+=1
            ix+=iy
            

    f.close()



if __name__ == "__main__":
    path1 =path+'/file/'

    Filelist = os.listdir(path1)
    print(Filelist)

    for i in range(0,len(Filelist)):
        x=MSHtran(Filelist[i])
        time.sleep(10)

