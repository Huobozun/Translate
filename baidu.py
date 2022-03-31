#coding=utf-8
import http.client
import hashlib
from urllib import parse
import random

def baidufanyi(word):

    appid = '20220321001133747'
    secretKey = '7UyMiEds7BCrDAoDjjBd'
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

    #file = open('result.txt','w')
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        _str = response.read().decode('utf-8')
        _str = eval(_str)
        """for line in _str['trans_result']:
            #file.write(line['dst']+'\n')
            print(line['dst'])
            xxx=line['dst']"""
        print(_str['trans_result'])
        xx1=_str['trans_result']
        xx2=xx1[0]
        xx3=xx2['dst']
        print(xx3)
        
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
    #file.close()
    return xx3

a='Apple is a great company'
aa=baidufanyi(a)
