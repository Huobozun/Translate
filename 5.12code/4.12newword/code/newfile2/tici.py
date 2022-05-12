
#将所有词条文件的词条、类型、来源依次提取出来放到相应的文件夹里面
from urllib import parse
import os

def get_filelist(dir):#依次遍历.json文件
 
    Filelist = []
 
    for home, dirs, files in os.walk(path):
 
        for filename in files:
 
            # 文件名列表，包含完整路径
            #Filelist.append(os.path.join(home, filename))
            # # 文件名列表，只包含文件名
            Filelist.append( filename)
    return Filelist

def getword(path):
    with open(path, 'r', encoding='utf-8') as f:
        data=[]
        title=[]
        for line in f:
            
                # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
                line = line.strip('\n').split('\t')  
                #print(line[0])
                #print(line[1])
                #print(line[2])
                #break
                #print(line)
                if(len(line)>1):
                    data.append(line[1])
                    title.append(line[0])
        #print(data[0])#此时data中的每个元素就是每行的第二列
        #抽出每行的单词
        data1=[]#将每行单词都排起来
        for i in range(0,len(data)):
            line0=data[i]
            data1.append([])
            word=''
            j=0
            while(j<len(line0)):
                if(len(line0)-j>7):
                    if(line0[j]==' 'and line0[j+1]=='['and line0[j+2]=='S'and line0[j+3]=='E'and line0[j+4]=='P'and line0[j+5]==']'and line0[j+6]==' '):
                        data1[i].append(word)
                        j+=7
                        word=''
                        continue
                if(j==len(line0)-1):
                    word+=line0[j]
                    data1[i].append(word)
                    j=len(line0)
                    word=''
                    continue
                else:
                    word+=line0[j]  
                    j+=1 
    return title,data1 #title是每行的title的list,对应的，data1是每行的英文单词的集合的list,data2是term type，data3是出处


path="D:\\ZJG\\zjg2\\4.12newword\\code\\newfile2"
Filelist=get_filelist(dir)
#_path="/home/zjg/code2/file/test1.tsv"

#print(a)

for ii in range(0,len(Filelist)):
    [at,ad]=getword('D:\\ZJG\\zjg2\\4.12newword\\code\\newfile2\\'+Filelist[ii])
    with open('D:\\ZJG\\zjg2\\4.12newword\\code\\newfile2\\word\\'+Filelist[ii],'w',encoding='utf-8')as f1:
        for ix in range(0,len(ad)):
            af=ad[ix]
            f1.write('%s\t%s\n' %(at[ix],af))
    f1.close()
