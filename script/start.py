import threading
import time
from script.backup import searchFiles
from script.rely import searchdir, proxies, ret


def __start(args,rooturl):
    time_1 = time.time()
    sem = threading.Semaphore(args.t)
    urlList = []
    urlList.extend(searchFiles(rooturl))

    if args.a:
        proxies['http'] = f"http://{args.a}"
        proxies['https'] = f"http://{args.a}"

    if args.b:
        sem = threading.Semaphore(5)
        searchdir(urlList,sem,rooturl)

    else:
        if not args.w:
            defaultword = './wordlist/default'
        else:
            defaultword = args.w

        f = open(defaultword, 'r')
        files = f.read().splitlines()
        for file in files:
            urlList.append(f'{rooturl}/{file}')
        f.close()
        searchdir(urlList,sem,rooturl)

    return (time_1,ret)