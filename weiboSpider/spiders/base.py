# coding:utf-8

from time import sleep

# from scrapy.spiders import Spider
# from scrapy.spidermiddlewares.httperror import HttpError
# # from scrapt import Request
# from twisted.internet.error import TimeoutError, TCPTimedOutError

from weiboSpider.database.handle import OperationRedis
from weiboSpider.data_type import DbTable
from weiboSpider.spiders.login import WeiboLogin


class BaseSpider(object):
    """
    爬虫基类
    """
    UID_TABLE = DbTable.REDIS_UID
    BID_TABLE = DbTable.REDIS_BID
    CID_TABLE = DbTable.REDIS_CID
    SID_TABLE = DbTable.REDIS_SID
    FOLID_TABLE = DbTable.REDIS_FOLID
    FANID_TABLE = DbTable.REDIS_FANID
    UID_LIST_TABLE = DbTable.REDIS_UID_LIST

    def __init__(self, redis_setting):
        self.redis_setting = redis_setting
        self.sleep_time = 2
        self.logger = None
        self._cookies = None
        self.__username = "12345678"
        self.__password = "12345678"
        self.__oper_redis = OperationRedis(redis_setting=self.redis_setting, logger=self.logger)

    def start_request(self):
        request = self.get_next_request()
        yield request

    def get_next_request(self):
        while True:
            uid = self._get_uid_from_redis()
            if uid:
                user_url = "https://weibo.com/u/{uid}".format(uid=uid)
                return user_url  #
                # return Request(user_url, callback=self.parse_user_info, errback=self.error_back, dont_filter=True)
            else:
                sleep(self.sleep_time)

    def error_back(self, failure):
        """
        错误处理
        :param failure:
        :return:
        """
        # self.logger.error(repr(failure))
        # if failure.check(HttpError):
        #     response = failure.value.response
        #     self.logger.error('HttpError on %s', response.url)
        #
        # elif failure.check(TimeoutError, TCPTimedOutError):
        #     request = failure.request
        #     self.logger.error('TimeoutError on %s', request.url)
        pass

    def crawl_done(self, uid):
        """
        该uid信息抓取完成
        :param uid:
        :return:
        """
        self.logger.info("用户所有信息抓取完成 ---> uid:%s" % uid)
        # 开始下一次抓取
        yield self.get_next_request()

    def crawl_fail(self, uid, tell_msg=None):
        """
        抓取失败
        :param uid:
        :param tell_msg:
        :return:
        """
        pass

    def __get_login_cookies(self):
        """
        获取登录cookies
        :return:
        """
        weibo = WeiboLogin()
        is_succ = weibo.login(username=self.__username, password=self.__password)
        if is_succ:
            self._cookies = weibo.cookies
            return True
        return False

    def _get_uid_from_redis(self):
        """
        从redis中取出一个uid
        :return:
        """
        return self.__oper_redis.get_uid()

    def _add_uid_to_redis(self, uid):
        """
        向redis中添加uid
        :param uid:
        :return:
        """
        self.__oper_redis.add_uid(uid=uid)

    def add_key_to_redis(self, table_type, key, value=None):
        """
        向redis中添加key，用于数据判重
        :param table_type:
        :param key:
        :param value:
        :return:
        """
        return self.__oper_redis.add_key(table_type=table_type, key=key, value=value)
