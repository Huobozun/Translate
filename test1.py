import re
import tiaoci
import tici
"""line=[['breast cancer','HER2 breast cancer','abdomen','abdomen neoplasm', 'abdomen tumors', 'abdomen tumours', 'Abdomen -- Tumors', 'Abdominal neoplasm NOS', 'abdominal neoplasm', 'Abdominal Neoplasms', 'Abdominal tumor', 'abdominal tumors', 'Abdominal tumour', 'abdominal tumours', 'abdominals tumors', 'Neoplasm of abdomen ( disorder )', 'Neoplasm of abdomen', 'Neoplasm , Abdominal', 'Neoplasms , Abdominal', 'tumor abdomen', 'tumor abdominal', 'tumor of abdomen', 'Tumour of abdomen']
,['Abetalipoproteinaemia', 'abetalipoproteinemia ( Bassen-Kornzweig )', 'abetalipoproteinemia ( diagnosis )', 'Abetalipoproteinemia ( disorder )', 'Abetalipoproteinemia', 'ABL - Abetalipoproteinaemia', 'ABL - Abetalipoproteinemia', 'Acanthocytoses', 'Acanthocytosis', 'Bassen Kornzweig Disease', 'Bassen Kornzweig syndrome', 'Bassen-Kornzweig Disease', 'Bassen-Kornzweig Syndrome', 'Bassen-Kornzweig', 'betalipoprotein deficiency disease', 'Betalipoprotein Deficiency Diseases', 'Deficiency Disease , Betalipoprotein', 'Deficiency Diseases , Betalipoprotein', 'Disease , Betalipoprotein Deficiency', 'Diseases , Betalipoprotein Deficiency', 'Homozygous familial hypobetalipoproteinaemia', 'Homozygous familial hypobetalipoproteinemia', 'microsomal triglyceride transfer protein deficiency disease', 'Microsomal Triglyceride Transfer Protein Deficiency', 'MTP DEFICIENCY']
,['Abnormal secretion of gastrin', 'abnormal ; gastrin secretion', 'Abnormality of secretion of gastrin ( finding )', 'Abnormality of secretion of gastrin', 'Gastrin secretion disorder NOS', 'Gastrin secretion disorder', 'gastrin ; secretion abnormal', 'secretion ; gastrin abnormal']
,['Brill Disease', 'Brill Zinsser disease ( diagnosis )', 'Brill Zinsser disease', 'Brill', "Brill 's Disease", 'Brill-Zinsser disease ( disorder )', 'Brill-Zinsser disease', 'Brills Disease', 'prowazekii ; Rickettsia prowazekii , typhus , recrudescent [ Brill-Zinsser ]', '#', 'Recrudescent typhus due to Rickettsia prowazekii', 'Recrudescent typhus fever', "Recrudescent typhus [ Brill 's disease ]", 'Recrudescent typhus', 'recrudescent [ Brill-Zinsser ] ; typhus', 'recrudescent [ Brill-Zinsser ] ; typhus , due to Rickettsia prowazekii', 'Rickettsia ; prowazekii , typhus , recrudescent [ Brill-Zinsser ]', 'typhus ; recrudescent [ Brill-Zinsser ]', 'typhus ; recrudescent [ Brill-Zinsser ] , due to Rickettsia prowazekii', 'typhus ; Rickettsia prowazekii , recrudescent [ Brill-Zinsser ]', 'Zinsser']
]

#去除缩写词条，并将缩写词条放入adsuo
ad5b=[]
for i in range(0,len(line)):
    ad5b.append(tiaoci._tiaocitong(line[i]))

print(ad5b)"""
"""#求去除缩写词条后的数量
num5=0
for i in range(0,len(ad5b)):
    b=ad4[i]
    c=ad5b[i]
    for j in range(0,len(b)):
        if(c[j]=='Y'):
            num5+=len(b[j])
print(num5)"""


"""
#line='prowazekii ; Rickettsia prowazekii , typhus , recrudescent [ Brill-Zinsser ]'
line='Selenium deficiency ( disorder )'
x='See++ low'
n = re.search(x,line)
#m = re.search(line,x)
#print(m)
print(n)
"""
"""#推断
line1=['Adenofibroma NOS', 'Adenofibroma', 'Adenofibromas', 'Benign adenofibroma ( morphologic abnormality )', 'Benign adenofibroma']
line2=tiaoci._tiaocitong2(line1)
print(line2)
num5=0
for i in range(0,len(line2)):
    c=line2[i]
    if(c=='Y'):
        num5+=len(line1[i])
    else:
        x=c[1]
        num5+=len(line1[i])-(x[1]-x[0]+1)

    
print(num5)
"""
"""line1=['Adenofibroma NOS abc', 'Adenofibroma', 'abc NOS, Adenofibroma','abc NOS;Adenofibroma','Adenofibromas', 'Benign adenofibroma ( morphologic abnormality )', 'Benign adenofibroma']
line=tiaoci._tiaocixiangsi(line1)
print(line)
print(int(5/3))"""


_path="/home/zjg/code2/file/Diseasr_or_Syndrome_All_AGGREGATED.tsv"
#_path="/home/zjg/code2/file/test1.tsv"
[at,ad0,ad2,ad3]=tici.getword(_path)

#1111111111去除重复的

ad0=[['abc','abc','ABC','abcd','abc','Abcd']]
ad2=[['1','2','3','4','5','6']]
ad1=[]
ad22=[]
for i in range(0,1):
    [x1,x2]=tiaoci._tiaocichongfu1(ad0[i],ad2[i])
    ad1.append(x1)
    ad22.append(x2)
print(len(ad1[0]),ad1[0])
print(len(ad22[0]),ad22[0])
adx1=[]
adx22=[]
for i in range(0,1):
    [x1,x2]=tiaoci._tiaocibold1(ad0[i],ad2[i])
    adx1.append(x1)
    adx22.append(x2)
print(len(adx1[0]),adx1[0])
print(len(adx22[0]),adx22[0])



"""#求去除重复后的数量
num1=0
for i in range(0,len(ad1)):
    b=ad1[i]
    for j in range(0,len(b)):
        c=b[j]
        num1+=len(c)
print('1去重复:',num1)"""

['breast cancer','HER2 breast cancer']
['Y',(0,(2,15))]#是否要翻译#不翻译的根据第几个词条推断#不翻译的内部的哪个位置需要用别的词条推断
['breast cancer','HER2 breast cancer']