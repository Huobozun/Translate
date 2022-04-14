import os 
import json
def get_title(name,file):
    with open('/home/zjg/code2/'+name+file,'r',encoding='utf-8')as ft:
        dataci=[]
        for line in ft:
            dataci.append(line)
        ft.close
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
        ft.close
        z=[]
        for ii in range(0,len(dataci)):
            x=dataci[ii]
            y=''
            for i in range(9,len(x)):
                y+=x[i]
            z.append(eval(y))
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
        ftitle=get_title('result-type/',Filelist[i])
        ft=get_content('result-type/',Filelist[i])
        fr=get_content('result-resouce/',Filelist[i])
        fp=get_content('result1/PNzh-',Filelist[i])
        fm=get_content('result2/MSHzh-',Filelist[i])
        with open('/home/zjg/code2/resultall1/'+Filelist[i],'w',newline='')as fa:
            for i1 in range(0,len(ft)):
                ft1=ft[i1]
                fr1=fr[i1]
                fp1=fp[i1]
                fm1=fm[i1]
                _grade=[]
                for i2 in range(0,len(ft1)):
                    _grade.append(0)
                    if(fr1[i2]=='MSH'):
                        _grade[i2]=1
                    if(ft1[i2]=='PN'):
                        _grade[i2]=2
                fa.write('%s\t' %(ftitle[i1]))
                _msh=0
                _pn=0
                for i3 in range(0,len(_grade)):
                    
                    if(_msh!=0 or _pn!=0):
                        if(_grade[i3]>0):
                            fa.write(' [SEP] ')
                    if(_grade[i3]==1):
                        fa.write('%s###%s###%s' %(fm1[_msh],ft1[i3],fr1[i3]))
                        _msh+=1
                    if(_grade[i3]==2):
                        fa.write('%s###%s###%s' %(fp1[_pn],ft1[i3],fr1[i3]))
                        _pn+=1
                    if(i3==len(_grade)-1):
                        fa.write('\n')
            fa.close








 