# coding:utf-8


class HttpData(object):
    HTTP_METHOD_GET = 1
    HTTP_METHOD_POST = 2
    HTTP_TIME_OUT = 10
    HTTP_DEFAULT_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    }

    def __init__(self):
        pass


if __name__ == '__main__':
    print(HttpData.HTTP_METHOD_GET)
