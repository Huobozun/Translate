

#仅提取文件中的titile和abstract
import json
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

def get_file(file):
    with open("/home/zjg/code3.31/pm1000-/"+file,'r',encoding='utf-8')as fr:
        with open("/home/zjg/code3.31/sampm2.3/Sam1-"+file,'w',encoding='utf-8',newline='')as fw:
            #data=json.load(fr)
            for lines in fr:
                lines=eval(lines)
                x=[]
                x.append(lines.get('title'))
                a=lines.get('abstract')
                for i in range(0,len(a)):
                    if(a[i].get('text')!=None):
                        x.append(a[i].get('text'))
                fw.write('%s\n' %(x))
            fw.close()
            fr.close()
            

if __name__=='__main__':
    path="/home/zjg/code3.31/pm1000-"
    Filelist=get_filelist(dir)
    for i in range(0,len(Filelist)):
        q=get_file(Filelist[i])
