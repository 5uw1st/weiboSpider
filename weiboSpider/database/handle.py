# coding:utf-8

import logging

from weiboSpider.database.mongodb import MongodbManage
from weiboSpider.database.redisdb import RedisManage
from weiboSpider.database.db_setting import MongodbName, DB_TABLE_RELATION
from weiboSpider.spiders.utils import handle_exception
from weiboSpider.tools.utils import get_timestamp

default_logger = logging


class InitDataToRedis(object):
    """
    将mongodb数据初始化到redis
    """
    def __init__(self, mongodb_setting, redis_setting, logger=default_logger):
        self.__mongodb_setting = mongodb_setting
        self.__redis_setting = redis_setting
        self.logger = logger
        self.mongodb_name = MongodbName.MONGODB_WEIBO_DB

    @handle_exception()
    def __get_mongodb_conn(self, table_name):
        """
        获取mongodb连接
        :param table_name:
        :return:
        """
        with MongodbManage(db_name=self.mongodb_name, collection=table_name,
                           mongo_setting=self.__mongodb_setting, logger=self.logger) as mongodb:
            return mongodb

    @handle_exception()
    def __get_redis_conn(self):
        """
        获取redis连接
        :return:
        """
        with RedisManage(redis_setting=self.__redis_setting, logger=self.logger) as redis:
            return redis

    @handle_exception()
    def __init_uid_info(self, redis_conn):
        """
        初始化用户ID
        :param redis_conn:
        :return:
        """
        db_relation = self._get_incidence_relation("USER_ID")
        mongodb_table = db_relation.get("MONGODB")
        redis_table = db_relation.get("REDIS")
        mongodb_conn = self.__get_mongodb_conn(table_name=mongodb_table)
        query = {}
        projection = {"uid": 1, "_id": 0}
        user_infos = mongodb_conn.select(query=query, projection=projection, to_list=False)
        with redis_conn.pipeline() as rpipe:
            for user in user_infos:
                key = user.get("uid")
                rpipe.hset(redis_table, key, get_timestamp())
            rpipe.execute()
            uid_count = redis_conn.hlen(redis_table)
            self.logger.info("--->成功初始化用户UID数据条数为:%d" % uid_count)
            return True

    @handle_exception()
    def __init_bid_info(self, redis_conn):
        """
        初始化微博ID
        :param redis_conn:
        :return:
        """
        db_relation = self._get_incidence_relation("BLOG_ID")
        mongodb_table = db_relation.get("MONGODB")
        redis_table = db_relation.get("REDIS")
        mongodb_conn = self.__get_mongodb_conn(table_name=mongodb_table)
        query = {}
        projection = {"uid": 1, "bid": 1, "_id": 0}
        blog_infos = mongodb_conn.select(query=query, projection=projection, to_list=False)
        with redis_conn.pipeline() as rpipe:
            for blog in blog_infos:
                key = "%s_%s" % (blog.get("uid"), blog.get("bid"))
                rpipe.hset(redis_table, key, get_timestamp())
            rpipe.execute()
            bid_count = redis_conn.hlen(redis_table)
            self.logger.info("--->成功初始化微博BID数据条数为:%d" % bid_count)
            return True

    @handle_exception()
    def __init_cid_info(self, redis_conn):
        """
        初始化评论ID
        :param redis_conn:
        :return:
        """
        db_relation = self._get_incidence_relation("COMMENT_ID")
        mongodb_table = db_relation.get("MONGODB")
        redis_table = db_relation.get("REDIS")
        mongodb_conn = self.__get_mongodb_conn(table_name=mongodb_table)
        query = {}
        projection = {"uid": 1, "bid": 1, "cid": 1, "_id": 0}
        comment_infos = mongodb_conn.select(query=query, projection=projection, to_list=False)
        with redis_conn.pipeline() as rpipe:
            for comment in comment_infos:
                key = "%s_%s_%s" % (comment.get("uid"), comment.get("bid"), comment.get("cid"))
                rpipe.hset(redis_table, key, get_timestamp())
            rpipe.execute()
            cid_count = redis_conn.hlen(redis_table)
            self.logger.info("--->成功初始化评论CID数据条数为:%d" % cid_count)
            return True

    @handle_exception()
    def __init_sid_info(self, redis_conn):
        """
        初始化分享人ID
        :param redis_conn:
        :return:
        """
        db_relation = self._get_incidence_relation("SHARE_ID")
        mongodb_table = db_relation.get("MONGODB")
        redis_table = db_relation.get("REDIS")
        mongodb_conn = self.__get_mongodb_conn(table_name=mongodb_table)
        query = {}
        projection = {"uid": 1, "bid": 1, "sid": 1, "_id": 0}
        share_infos = mongodb_conn.select(query=query, projection=projection, to_list=False)
        with redis_conn.pipeline() as rpipe:
            for share in share_infos:
                key = "%s_%s_%s" % (share.get("uid"), share.get("bid"), share.get("sid"))
                rpipe.hset(redis_table, key, get_timestamp())
            rpipe.execute()
            sid_count = redis_conn.hlen(redis_table)
            self.logger.info("--->成功初始化分享SID数据条数为:%d" % sid_count)
            return True

    @handle_exception()
    def __init_folid_info(self, redis_conn):
        """
        初始化关注人ID
        :param redis_conn:
        :return:
        """
        db_relation = self._get_incidence_relation("FOLLOW_ID")
        mongodb_table = db_relation.get("MONGODB")
        redis_table = db_relation.get("REDIS")
        mongodb_conn = self.__get_mongodb_conn(table_name=mongodb_table)
        query = {}
        projection = {"uid": 1, "folid": 1, "_id": 0}
        follow_infos = mongodb_conn.select(query=query, projection=projection, to_list=False)
        with redis_conn.pipeline() as rpipe:
            for follow in follow_infos:
                key = "%s_%s" % (follow.get("uid"), follow.get("folid"))
                rpipe.hset(redis_table, key, get_timestamp())
            rpipe.execute()
            folid_count = redis_conn.hlen(redis_table)
            self.logger.info("--->成功初始化关注人FOLID数据条数为:%d" % folid_count)
            return True

    @handle_exception()
    def __init_fanid_info(self, redis_conn):
        """
        初始化粉丝ID
        :param redis_conn:
        :return:
        """
        db_relation = self._get_incidence_relation("FAN_ID")
        mongodb_table = db_relation.get("MONGODB")
        redis_table = db_relation.get("REDIS")
        mongodb_conn = self.__get_mongodb_conn(table_name=mongodb_table)
        query = {}
        projection = {"uid": 1, "fanid": 1, "_id": 0}
        fan_infos = mongodb_conn.select(query=query, projection=projection, to_list=False)
        with redis_conn.pipeline() as rpipe:
            for fan in fan_infos:
                key = "%s_%s" % (fan.get("uid"), fan.get("fanid"))
                rpipe.hset(redis_table, key, get_timestamp())
            rpipe.execute()
            fanid_count = redis_conn.hlen(redis_table)
            self.logger.info("--->成功初始化粉丝FANID数据条数为:%d" % fanid_count)
            return True

    def _get_incidence_relation(self, table_type):
        """
        获取mongodb与redis表之间的关联关系
        :param table_type:
        :return:
        """
        return DB_TABLE_RELATION.get(table_type)

    @handle_exception()
    def start(self):
        """
        开始初始化
        :return:
        """
        redis_conn = self.__get_redis_conn()

        is_init_succ = self.__init_uid_info(redis_conn)
        if not is_init_succ:
            self.logger.debug("<--初始化用户信息失败")
            return False

        is_init_succ = self.__init_bid_info(redis_conn)
        if not is_init_succ:
            self.logger.debug("<--初始化微博信息失败")
            return False

        is_init_succ = self.__init_cid_info(redis_conn)
        if not is_init_succ:
            self.logger.debug("<--初始化评论信息失败")
            return False

        is_init_succ = self.__init_sid_info(redis_conn)
        if not is_init_succ:
            self.logger.debug("<--初始化分享信息失败")
            return False

        is_init_succ = self.__init_folid_info(redis_conn)
        if not is_init_succ:
            self.logger.debug("<--初始化关注人信息失败")
            return False

        is_init_succ = self.__init_fanid_info(redis_conn)
        if not is_init_succ:
            self.logger.debug("<--初始化粉丝信息失败")
            return False

        self.logger.info("--->所有数据初始化成功")
        return True
