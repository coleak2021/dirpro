#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Author: coleak
version: 1.1
'''

import argparse
from script.end import __end
from script.start import __start


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='dirscan,The top10000 dir is scanned by default')
    parser.add_argument('-u', type=str, help='url')
    parser.add_argument('-t', type=int, default=30, help='thread:default=30')
    parser.add_argument('-w', type=str, help='dirfile path')
    parser.add_argument('-a', type=str, help='proxy,such as 127.0.0.1:7890')
    parser.add_argument('-f', type=str, help='urlfile,urls in the file')
    parser.add_argument('-b', action='store_true', help='fastly to find backup files and sensitive files')
    args = parser.parse_args()
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
    if not args.f:
        rooturl = args.u.strip('/')
        (time1,ret)=__start(args,rooturl)
        __end(rooturl,time1,ret)
    else:
        urlfile=open(args.f, 'r')
        urls = urlfile.read().splitlines()
        for rooturl in urls:
            rooturl = rooturl.strip('/')
            (time1,ret) = __start(args, rooturl)
            __end(rooturl,time1,ret)

    # time1 = time.time()
    # rooturl=args.u.strip('/')
    # urlList = []
    # urlList.extend(searchFiles(rooturl))

    # if args.a:
    #     proxies['http'] = f"http://{args.a}"
    #     proxies['https'] = f"http://{args.a}"
    #
    # if args.b:
    #     sem = threading.Semaphore(5)
    #     searchdir(urlList)
    #
    # else:
    #     if not args.w:
    #         defaultword='./wordlist/default'
    #     else:
    #         defaultword=args.w
    #
    #     f = open(defaultword, 'r')
    #     files=f.read().splitlines()
    #     for file in files:
    #         urlList.append(f'{rooturl}/{file}')
    #     f.close()
    #     searchdir(urlList)
    #
    # result=__Results(rooturl,ret)
    # time2 = time.time()
    # print("总共花费: ", time2 - time1,"秒,",f"结果保存在{result}")