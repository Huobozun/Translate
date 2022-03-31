from base64 import encode
from email.quoprimime import unquote
import re 
import tiaoci
import fanyibaidu
import tici
import urllib
#from urllib import quote
#from urllib import unquote

from urllib.parse import quote


#really;;;basketball;;; 翻译会直接合起来
#really\tbasketball\t 翻译会直接合起来
#really\nbasketball\n 翻译会只翻译第一行
#可以实现的有'#''%''￥''$'
#'#%'＞'%#'＞'#'或'%'
#7个以内比较准确
#数字效果最好，因为数字是直译,便于揪出来对应.数字也是7个以内准确，但是有意外多出一个词的情况
#resu+='!'+label[i]+'>998'200个list里面只有11个数量对不上。可以在数量对不上的时候再挑出来去单独翻译
#resu+='!'+label[i]+'>9,8'目前效果最好，200个list里面只有8个数量对不上。可以在数量对不上的时候再挑出来去单独翻译

#官方文件说\n可以拼接多个字段，确实OK


"""
line1=['Agricultural Worker Disease', 'Agricultural Worker Diseases', "Agricultural Worker 's Disease", "Agricultural Worker 's Diseases", 'Agricultural Workers Disease', 'Agricultural Workers Diseases', "Agricultural Workers ' Disease", "Agricultural Workers ' Diseases", 'Disease , Agricultural Worker', "Disease , Agricultural Worker 's", "Disease , Agricultural Workers '", 'Diseases , Agricultural Worker', "Diseases , Agricultural Worker 's", "Diseases , Agricultural Workers '", 'Worker Disease , Agricultural', 'Worker Diseases , Agricultural', "Worker 's Disease , Agricultural", "Worker 's Diseases , Agricultural", "Workers ' Disease , Agricultural", "Workers ' Diseases , Agricultural"]
for i in range(3,len(line1)):
    line0=[]
    for j in range(0,i):
        line0.append(line1[j])

    x1=''
    x1+=tiaoci._tiaocihebing(line0)
    #print(x1)
    print(len(line0))
    lines2=fanyibaidu.baidufanyi(x1)
    #print(lines2)
    print(len(lines2))"""

"""_path="/home/zjg/code2/file/Diseasr_or_Syndrome_All_AGGREGATED.tsv"
#_path="/home/zjg/code2/file/test1.tsv"
[at,ad]=tici.getword(_path)
#print(a)
W=0
for ii in range(0,100):
    line1=ad[ii]
   
    x1=''
    x1+=tiaoci._tiaocihebing(line1)
    #print(x1)
    #print(len(line1))
    lines2=fanyibaidu.baidufanyi(x1)
    #print(lines2)
    if(len(lines2)!=len(line1)):
        W+=1
        print('WRONG:',W)
        print(line1)
"""

line1=['EGFR NM_005228.5:c.2224G>A']
x1=''
x1+=tiaoci._tiaocihebing(line1)
    #print(x1)
    #print(len(line1))
lines2=fanyibaidu.baidufanyi(x1,1)
print(lines2)