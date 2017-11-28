# coding:utf-8

import logging

from redis import Redis

from weiboSpider.database.db_setting import REDIS_SETTING
from weiboSpider.tools.utils import Singleton

default_redis_setting = REDIS_SETTING["LOCAL"]
default_logger = logging


class RedisManage(Singleton):
    """
    redis管理
    """
    def __init__(self, redis_setting=default_redis_setting, logger=default_logger):
        self.__host = redis_setting.get("host")
        self.__port = redis_setting.get("port")
        self.__db = redis_setting.get("db")
        self.__password = redis_setting.get("password")
        self.logger = logger
        self.conn = None
        self.__init_conn()

    def __init_conn(self):
        if not self.conn:
            self.conn = Redis(
                host=self.__host,
                port=self.__port,
                db=self.__db,
                password=self.__password,
            )
            self.logger.info("连接redis成功")

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == '__main__':
    with RedisManage() as rt:
        rt.set("test", "121313")

