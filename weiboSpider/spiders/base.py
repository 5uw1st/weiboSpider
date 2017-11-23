# coding:utf-8

from weiboSpider.database.redisdb import RedisManage


class BaseSpider(object):
    """
    爬虫基类
    """

    def __init__(self):
        pass

    def get_start_request(self):
        pass

    def get_uid_from_redis(self):
        """
        从redis中取出一个uid
        :return:
        """
        pass
