

#从文章中用AC自动机查找词典中的词出现的频率
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

def file_word(file):
     #读入要查找词的文件
    data=''
    with open("/home/zjg/code3.31/sampm2.3/"+file,'r',encoding='utf8')as fr:  
        for lines in fr:
            json_data=lines
            data+=str(json_data)
        fr.close()
    return data#data就是一个文件的所有内容的str形式

def frefile(filedata,label):
    A = ahocorasick.Automaton()

    # 向trie树中添加单词
    for index,word in enumerate(label):
        A.add_word(word, (index, word))
    # 用法分析add_word(word,[value]) => bool
    # 根据Automaton构造函数的参数store设置，value这样考虑：
    # 1. 如果store设置为STORE_LENGTH，不能传递value，默认保存len(word)
    # 2. 如果store设置为STORE_INTS，value可选，但必须是int类型，默认是len(automaton)
    # 3. 如果store设置为STORE_ANY，value必须写，可以是任意类型
    # 将trie树转化为Aho-Corasick自动机
    A.make_automaton()



    #设置计数list
    yy=[]
    for i in range(0,len(label)):
        yy.append(0)

    #每个文件读取查找
    for item in A.iter(filedata):
        y=item[1]#比对查找结果
        ii=y[0]
        yy[ii]+=1  
    return yy


"""    for i in range(0,len(filedata)):
        data1=filedata[i]#读入每行
        for j in range(0,len(data1)):
            word=data1.get('%s'%(j))#读入每段进行查找
            if(word==None):
                word=' '
            for item in A.iter(word):
                y=item[1]#比对查找结果
                for ii in range(0,len(x)):
                    if(y[1]==x[ii]):
                        yy[ii]+=1"""

"""    #每行读取查找
    for i in range(0,len(filedata)):
        data1=filedata[i]#读入每行
        for j in range(0,len(data1)):
            word=data1.get('%s'%(j))#读入每段进行查找
            if(word==None):
                word=' '
            for item in A.iter(word):
                y=item[1]#比对查找结果
                for ii in range(0,len(x)):
                    if(y[1]==x[ii]):
                        yy[ii]+=1"""
"""    with open('fre.tsv','a',encoding='utf8')as fw:
        fw.write('%s\n'%(yy))
        fw.close"""
    #return yy

if __name__ == "__main__":
    #读入文章列表
    path ="/home/zjg/code3.31/sampm2.3"
    Filelist = get_filelist(dir)
    #print(Filelist)
    path ="/home/zjg/code3.31/result-word"
    Filelistword = get_filelist(dir)
    for ida in range(0,len(Filelist)):
    #for ida in range(0,1):
        #读入文件中的数据（文件夹中的所有文件的title和text）
        filedata=file_word(Filelist[ida])

        for iff in range(0,len(Filelistword)):
        #for iff in range(0,2):
            #读入要查找频率的词条
            with open('/home/zjg/code3.31/result-word/'+Filelistword[iff],'r',encoding='utf-8')as fc:
                dataci=[]
                for line in fc:
                    dataci.append(line)
                fc.close()
            z=[]
            for ii in range(0,len(dataci)):
                x=dataci[ii]
                y=''
                for i in range(9,len(x)):
                    y+=x[i]
                z.append(eval(y))
            #z是读取完之后为list[['','',''],[]]格式
        
        
            #按照每篇所有单词依次进行词条在所有文章的出现频率
            with open('/home/zjg/code3.31/fre/fre2.3/'+Filelistword[iff].replace('.tsv','')+'/fre0-'+Filelist[ida].replace('.json','')+Filelistword[iff],'w',encoding='utf-8')as ff:
                ix=0
                while(ix<len(z)):
                    word=[]
                    iy=0
                    while(iy<len(z) and ix+iy<len(z)):
                        zz=z[ix+iy]
                        for j in range(0,len(z[ix+iy])):
                            word.append(zz[j])  
                        iy+=1
                    a=frefile(filedata,word)
                    i=0
                    i2=ix
                    while(i<len(a)):
                        freres=[]
                        for jj in range(0,len(z[i2])):
                            freres.append(a[i+jj])
                        ff.write('%s\n' %(json.dumps(freres)))
                        i+=len(z[i2])
                        i2+=1
                    ix+=iy
                ff.close()