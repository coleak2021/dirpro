import os
import random
from threading import Thread
import requests

#存放响应信息
ret = []

#进度条计算参数
_list=[]
d=0

#代理
proxies={}

#线程控制
_sem=None

#随机agent头
def __random_agent():
    user_agent_list = [
            {'User-Agent': 'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; en) Opera 11.00'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.2) Gecko/2008092313 Ubuntu/8.04 (hardy) Firefox/3.0.2'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.15) Gecko/20101027 Fedora/3.5.15-1.fc12 Firefox/3.5.15'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.551.0 Safari/534.10'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.2) Gecko/2008092809 Gentoo Firefox/3.0.2'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.544.0'},
            {'User-Agent': 'Opera/9.10 (Windows NT 5.2; U; en)'},
            {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko)'},
            {'User-Agent': 'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9b3) Gecko/2008020514 Firefox/3.0b3'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.60'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.366.0 Safari/533.4'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.51'}
        ]
    return random.choice(user_agent_list)

# 发送请求
def __get(url):
    count = 0
    global d
    with _sem:
        while count < 3:
            try:
                r = requests.get(url,headers=__random_agent(),proxies=proxies)
            except:
                count += 1
                continue
            break

    #判断请求是否成功
    if count >= 3:
        print(f'visit failed:{url}')
        return

    l=len(r.text)
    if r.status_code != 404 and r.status_code != 429:
        log = f'{r.status_code:<6}{l:<7}{url}'
        print(log)
    elif r.status_code == 429:
        print('Too Many Requests 429 so that Request terminated,please Set up smaller threads')
        os._exit(0)

    d += 1
    if d in _list:
        print(f"[*]已经扫描{(_list.index(d)+1)*10}%")

    # 添加到ret
    ret.append({
        'status_code': r.status_code,
        'length': l,
        'url': url
    })



def searchdir(urlList,sem,rooturl):
    global d
    global _sem
    global _list
    d=0
    _sem=sem
    thread_array = []
    n=len(urlList)
    k=int (n/10)
    for i in range(1,10):
        _list.append(k*i)
    print(f"[*]开始扫描{rooturl}")
    for i in urlList:
        t = Thread(target= __get,args=(i,))
        thread_array.append(t)
        t.start()
    for t in thread_array:
        t.join()