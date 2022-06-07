
#申请的百度免费版API,用百度API的id和secretKey填到15、16行
#调用形式为 lines2=fanyibaidu.baidufanyi(af1,il)，af1是'one\ntwo\n',il是词的个数2（\n区分两个词条），返回['一','二']

import http.client
import hashlib
from urllib import parse
import random
import time
import os
path = os.getcwd()


def baidufanyi(word,_len):

    appid = ''
    secretKey = ''
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q =word
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign 

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        _str = response.read().decode('utf-8')
        if(_str!=''):
            _str = eval(_str)

            if(len(_str['trans_result'])==1):
                xx3=[]
                xx1=_str['trans_result']
                xx2=xx1[0]
                xx3.append(xx2['dst'])
            else:
                xx1=_str['trans_result']
                xx3=[]
                for i in range(0,len(xx1)):
                    xx2=xx1[i]
                    xx3.append(xx2['dst'])
        else:#第一次翻译出错
            time.sleep(1)
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            _str = response.read().decode('utf-8')
            if(_str!=''):
                _str = eval(_str)

                if(len(_str['trans_result'])==1):
                    xx3=[]
                    xx1=_str['trans_result']
                    xx2=xx1[0]
                    xx3.append(xx2['dst'])
                else:
                    xx1=_str['trans_result']
                    xx3=[]
                    for i in range(0,len(xx1)):
                        xx2=xx1[i]
                        xx3.append(xx2['dst'])
            else:#第二次翻译出错
                xx3=[]
                for i in range(0,_len):
                    xx3.append('翻译出错')

    except Exception as e:

        time.sleep(1.5)#0.7在range0-3可以进行
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        _str = response.read().decode('utf-8')
        if(_str!='' and _str[0]!="<"):

            _str = eval(_str)
            if(len(_str['trans_result'])==1):
                xx3=[]
                xx1=_str['trans_result']
                xx2=xx1[0]
                xx3.append(xx2['dst'])
            else:
                xx1=_str['trans_result']
                xx3=[]
                for i in range(0,len(xx1)):
                    xx2=xx1[i]
                    xx3.append(xx2['dst'])
        else:#第一次翻译出错
            time.sleep(1.2)
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            _str = response.read().decode('utf-8')
            if(_str!='' and _str[0]!="<"):
                _str = eval(_str)

                if(len(_str['trans_result'])==1):
                    xx3=[]
                    xx1=_str['trans_result']
                    xx2=xx1[0]
                    xx3.append(xx2['dst'])
                else:
                    xx1=_str['trans_result']
                    xx3=[]
                    for i in range(0,len(xx1)):
                        xx2=xx1[i]
                        xx3.append(xx2['dst'])
            else:#第二次翻译出错
                xx3=[]
                for i in range(0,_len):
                    xx3.append('翻译出错')
    finally:
        if httpClient:
            httpClient.close()
    return xx3


