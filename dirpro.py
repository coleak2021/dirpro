#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: coleak
version: 1.0
'''
import os
import random
import sys
import time
import argparse
from threading import Thread
import threading
from script.backup import searchFiles
import requests
from script.results import __Results

#存放响应信息
ret = []

#进度条计算参数
_list=[]
d=0

#代理
proxies={}


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
    with sem:
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

def searchdir(urlList):
    thread_array = []
    n=len(urlList)
    k=int (n/10)
    for i in range(1,10):
        _list.append(k*i)
    print("[*]开始扫描")
    for i in urlList:
        t = Thread(target= __get,args=(i,))
        thread_array.append(t)
        t.start()
    for t in thread_array:
        t.join()





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dirscan,The top10000 dir is scanned by default')
    parser.add_argument('-u', type=str, help='url')
    parser.add_argument('-t', type=int, default=30, help='thread:default=30')
    parser.add_argument('-w', type=str, help='dirfile path')
    parser.add_argument('-a', type=str, help='proxy,such as 127.0.0.1:7890')
    parser.add_argument('-b', action='store_true', help='fastly to find backup files and sensitive files')
    args = parser.parse_args()
    sem = threading.Semaphore(args.t)
    print(r'''
  __                                    
 /\ \  __                               
 \_\ \/\_\  _ __   _____   _ __   ___   
 /'_` \/\ \/\`'__\/\ '__`\/\`'__\/ __`\ 
/\ \L\ \ \ \ \ \/ \ \ \L\ \ \ \//\ \L\ \
\ \___,_\ \_\ \_\  \ \ ,__/\ \_\\ \____/
 \/__,_ /\/_/\/_/   \ \ \/  \/_/ \/___/ 
                     \ \_\              
                      \/_/      
''')

    time1 = time.time()
    rooturl=args.u.strip('/')
    urlList = []
    urlList.extend(searchFiles(rooturl))

    if args.a:
        proxies['http'] = f"http://{args.a}"
        proxies['https'] = f"http://{args.a}"

    if args.b:
        sem = threading.Semaphore(5)
        searchdir(urlList)

    else:
        if not args.w:
            defaultword='./wordlist/default'
        else:
            defaultword=args.w

        f = open(defaultword, 'r')
        files=f.read().splitlines()
        for file in files:
            urlList.append(f'{rooturl}/{file}')
        f.close()
        searchdir(urlList)

    result=__Results(rooturl,ret)
    time2 = time.time()
    print("总共花费: ", time2 - time1,"秒,",f"结果保存在{result}")