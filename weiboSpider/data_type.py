# coding:utf-8


class HttpData(object):
    HTTP_METHOD_GET = 1
    HTTP_METHOD_POST = 2
    HTTP_TIME_OUT = 10
    HTTP_DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    }


class DbTable(object):
    REDIS_UID = 1
    REDIS_BID = 2
    REDIS_CID = 3
    REDIS_SID = 4
    REDIS_FOLID = 5
    REDIS_FANID = 6
    REDIS_UID_LIST = 7

