

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




if __name__=='__main__':

    path ="D:\\ZJG\\ZJG2\\resultall_final\\ALL_RESULT_zh\\"

    Filelist = get_filelist(dir)
    print(Filelist)
    for i in range(0,len(Filelist)):

        with open("D:\\ZJG\\ZJG2\\resultall_final\\ALL_RESULT_zh\\"+Filelist[i],'r',encoding='utf-8')as fr:
            with open('D:\\ZJG\\ZJG2\\resultall_final2.0\\ALL_RESULT_zh\\'+Filelist[i],'w',encoding='utf-8',newline='')as fw:
                for lines in fr:
                    i1=0
                    while(i1<len(lines)):
                        if(i1<len(lines)-1):
                            if(lines[i1]+lines[i1+1]!="\\" ):
                                if(lines[i1]+lines[i1+1]!="\/"):

                                    fw.write('%s' %(lines[i1]))
                                    i1+=1
                                else:
                                    i1+=1
                            else:
                                i1+=2
                        else:
                            fw.write('%s' %(lines[i1]))
                            i1+=1

            fw.close()
        fr.close()
