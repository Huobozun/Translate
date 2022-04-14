import os 
import json
import sys
sys.path.append('/home/zjg/code2/')
import fanyibaidu
def get_title(name,file):
    with open(name+file,'r',encoding='utf-8')as ft:
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
    with open(name+file,'r',encoding='utf-8')as ft:
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



if __name__ == "__main__":

    file='pharmcube.tsv'
    ftitle=get_title('D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\filenew\\',file)#list里类型为str
    fw1=get_content('D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\filenew\\',file)#list里类型为list

    with open("D:\\ZJG\\zjg2\\4.12newword\\code\\fanyiword\\file2\\"+file,'w',encoding='utf-8')as fw:
        i=0
        while(i<len(ftitle)):
            fw.write('%s\t%s\n' %(ftitle[i],fw1[i]))
            i+=1
        fw.close()

   







