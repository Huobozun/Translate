#本文件是将100个文件的词条出现次数加起来形成一个文件
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

def file_fre(file,ii):
     #读入文件频率
    data=[]
    with open('/home/zjg/code3.31/result-fre-2years/'+file.replace('.tsv','')+'/fre-Sam-'+str(ii)+file,'r',encoding='utf-8')as fii:
        for lines in fii:
            json_data=lines
            data.append(eval(json_data))
        fii.close()
    return data#data就是一个文件的所有频率

def add_fre(a,file,ii):
     #将两个文件频率求和
    data=[]
    with open('/home/zjg/code3.31/result-fre-2years/'+file.replace('.tsv','')+'/fre-Sam-'+str(ii)+file,'r',encoding='utf-8')as fii:
        for lines in fii:
            json_data=lines
            data.append(eval(json_data))
        fii.close()
    ae=[]
    for i in range(0,len(a)):
        a1=a[i]
        data1=data[i]
        for j in range(0,len(a1)):
            a1[j]+=data1[j]
        ae.append(a1)
    return ae#ae是求和后的结果


if __name__ == "__main__":
    #读入文章列表
    path ="/home/zjg/code3.31/result-word/"
    Filelist = get_filelist(dir)
    for i in range(0,len(Filelist)):#每一类的文件求和
    #for i in range(0,1):
        for ii in range(0,100):#读取每一个文件依次累加
            if(ii==0):
                a=file_fre(Filelist[i],ii)
            else:
                a=add_fre(a,Filelist[i],ii)
        #加完之后写入总的文件
        with open('/home/zjg/code3.31/result-fre-2years/'+'All-'+Filelist[i],'w',newline='')as fw:
            for iw in range(0,len(a)):
                fw.write('%s\n' %(json.dumps(a[iw])))
            fw.close()