


import json
import os
import ahocorasick


def get_filelist(dir):#依次遍历.json文件
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 
            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist


def file_fre(file):
     #读入文件频率
    data=[]
    with open('/home/zjg/code2/code3.31/result-fre3/'+'All-'+file,'r',encoding='utf-8')as fii:
        for lines in fii:
            json_data=lines
            data.append(eval(json_data))
        fii.close()
    return data#data就是一个文件的所有频率

def file_word(file):
     #读入文件词条
    with open('/home/zjg/code2/result-word/'+file,'r',encoding='utf-8')as fc:
        dataci=[]
        for line in fc:
            dataci.append(line)
        fc.close()
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
    
        
    return t,z#t是title的list,z是词条的list



if __name__ == "__main__":
    #读入文章列表
    path ="/home/zjg/code2/result-word/"
    Filelist = get_filelist(dir)
    with open('/home/zjg/code2/resultfre1/0countnumber.tsv','w',newline='')as fcc0:
        y=0
        for i in range(0,len(Filelist)):#每个文件
        #for i in range(0,1):
            a=file_fre(Filelist[i])
            [t,w]=file_word(Filelist[i])
            count=[]
            with open('/home/zjg/code2/resultfre1/Cfre-'+Filelist[i],'w',newline='')as fw0:
                with open('/home/zjg/code2/resultfre1/Hfre-'+Filelist[i],'w',newline='')as fw1:
                    x=0
                    for j in range(0,len(a)):#每行
                        a1=a[j]
                        t1=t[j]
                        w1=w[j]
                        count.append([])
                        wplus=[]
                        for jj in range(0,len(a1)):
                            if(a1[jj]>=10):#挑出出现次数大于等于10的词条
                                count[j].append(jj)
                                wplus.append(w1[jj])
                        fw1.write('%s\t%s\n' %(t1,wplus))#记录文件名和词条
                        fw0.write('%s\t%s\n' %(t1,count[j]))#记录文件名和词条位置
                        x+=len(count[j])
                    fw1.close()
                    fw0.close()
            y+=x
            fcc0.write('%s\t%s\n' %(Filelist[i],x))#词条总数
            print(Filelist[i],' ',x)
        fcc0.write('Total:\t%s\n' %(y))#词条总数
        fcc0.close()
        print('Total:',y)
                    




    

