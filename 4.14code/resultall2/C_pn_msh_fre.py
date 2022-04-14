import os 
import json
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
    for i in range(0,len(Filelist)):

        ftitle=get_title('result-type/',Filelist[i])#list里类型为str
        ft=get_content('result-type/',Filelist[i])#list里类型为list
        fr=get_content('result-resouce/',Filelist[i])#list里类型为list
        ff=get_content('resultfre1/resultfre&baidu/Hfre-zh-',Filelist[i])#list里类型为list
        fc=get_index('resultfre1/Cfre-',Filelist[i])#list里类型为list
        fword=get_word('resultall1/',Filelist[i])#list里类型为str
        with open('/home/zjg/code2/resultall2/Mark_word1/M10-'+Filelist[i],'w',newline='')as fa:
            x=[]
            for i1 in range(0,len(ft)):
                x.append([])
                x1=x[i1]
                ft1=ft[i1]
                fr1=fr[i1]
                ff1=ff[i1]
                fc1=fc[i1]
                fword1=fword[i1]
                fword1=fword1.replace('\n','')
                for i11 in range(0,len(fr1)):
                    if(fr1[i11]=='MSH' or ft1[i11]=='PN'):
                        x1.append(1)#MSH和PN翻译过，记为1
                    else:
                        x1.append(0)#其他没翻译的记为0
                for i2 in range(0,len(fc1)):
                    if(ft1[int(fc1[i2])]!='PN' and fr1[int(fc1[i2])]!='MSH'):#出现次数高的词为PN或者MSH就不再添加，否则添加
                        x1[int(fc1[i2])]=1#频率高的需要翻译，并且不是PN和MSH的改为1
                fa.write('%s\t%s\n' %(ftitle[i1],x1))#重新写进新的文件
            fa.close()








 