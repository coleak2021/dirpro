import time
from script.results import __Results
def __end(rooturl,time1,ret):
    result = __Results(rooturl,ret)
    time2 = time.time()
    print("总共花费: ", time2 - time1, "秒,", f"结果保存在{result}")
    ret.clear()