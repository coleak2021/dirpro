# 处理搜索结果
import time


def __Results(rooturl,ret):
    print("[*]扫描完成，正在根据长度和状态码整理扫描结果")
    t=f"./scan_result/{rooturl.split('//')[1].replace(':', '').replace('/', '')}{int (time.time())}"
    try:
        f = open(t, 'w',encoding="utf-8")
    except:
        f = open(f"{int (time.time())}", 'w',encoding="utf-8")
    f.write(f"扫描结束时间{time.strftime('%m-%d--%H:%M:%S')}")
    f.write('\n')
    def __log(s):
        print(s)
        f.write(s)
        f.write('\n')
    statusCodeMap = {}
    lenMap = {}
    for result in ret:
        statusCode = result['status_code']
        length = result['length']
        statusCodeMap[statusCode] = statusCodeMap.get(statusCode, 0) + 1
        lenMap[length] = lenMap.get(length, 0) + 1
    # 打印状态异常
    maxStatusCode = -1
    maxStatusCodeCount = -1
    for statusCode, count in statusCodeMap.items():
        if maxStatusCodeCount < count:
            maxStatusCodeCount = count
            maxStatusCode = statusCode
    __log('-----------unnormal status:')
    for result in ret:
        if result['status_code'] != maxStatusCode:
            __log(f'{result["status_code"]:<6}{result["length"]:<7}{result["url"]}')
    # 打印长度异常
    maxLength = -1
    maxLengthCount = -1
    for length, count in lenMap.items():
        if maxLengthCount < count:
            maxLengthCount = count
            maxLength = length
    __log('-----------unnormal length:')
    for result in ret:
        if result['length'] != maxLength:
            __log(f'{result["status_code"]:<6}{result["length"]:<7}{result["url"]}')
    f.close()
    return t