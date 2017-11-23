# coding:utf-8

import logging
from pymongo import MongoClient

from weiboSpider.database.db_setting import MONGODB_SETTING

default_mongo_setting = MONGODB_SETTING["LOCAL"]
default_logger = logging


class MongodbManage(object):
    """
    Mongodb管理
    """
    def __init__(self, db_name, collection, mongo_setting=default_mongo_setting, logger=default_logger):
        self.__host = mongo_setting.get("host")
        self.__port = mongo_setting.get("port")
        self.__username = mongo_setting.get("username")
        self.__password = mongo_setting.get("password")
        self._db_name = db_name
        self._table = collection
        self.logger = logger
        self.client = None
        self.collection = None
        self.__init_conn()

    def __init_conn(self):
        """
        初始化mongo连接
        :return:
        """
        if not self.client:
            self.client = MongoClient(
                host=self.__host,
                port=self.__port,
            )
        db = self.client[self._db_name]
        if self.__username and self.__password:
            db.authenticate(name=self.__username, password=self.__password)
        self.collection = db.get_collection(self._table)
        self.logger.info("连接mongodb成功:host --> %s:%d" % (self.__host, self.__port))

    def insert(self, data, query=None, allow_repeat=False):
        """
        插入数据
        :param data:
        :param query:
        :param allow_repeat:
        :return:
        """
        uid_list = []
        if not isinstance(data, list):
            data = [data]
        for data_one in data:
            need_insert = True
            if query:
                count = self.collection.find(query).count()
                if count > 0 and allow_repeat:
                    self.logger.info("存在%d条相同数据,allow_repeat:%s" % (count, str(allow_repeat)))
                else:
                    need_insert = False
            self.logger.info("是否需要插入该数据:%s" % str(need_insert))
            if need_insert:
                uid = self.collection.insert_one(data_one).inserted_id
                self.logger.info("插入数据成功:%s" % uid)
                uid_list.append(uid)
        msg = "--->总数据:%d,成功插入:%d,重复数据:%d" % (len(data), len(uid_list), (len(data)-len(uid_list)))
        self.logger.info(msg)
        return uid_list

    def select(self, query, projection=None, to_list=True):
        """
        查询数据
        :param query:
        :param projection:
        :param to_list:
        :return:
        """
        query_ret = self.collection.find(query, projection=projection)
        count = query_ret.count()
        self.logger.info("--->成功查询到%s条数据" % count)
        if to_list:
            self.logger.info("查询数据已转换为list")
            return [i for i in query_ret]
        return query_ret

    def update(self, query, set_data, upsert=True):
        """
        更新数据
        :param set_data:
        :param query:
        :param upsert:
        :return:
        """
        ret = self.collection.update_many(query, update=set_data, upsert=upsert)
        modified_count = ret.modified_count
        self.logger.info("--->存在%d条数据,更新%d条数据" % (ret.matched_count, modified_count))
        return modified_count

    def delete(self, query, multi=True):
        """
        删除数据
        :param query:
        :param multi:
        :return:
        """
        ret = self.collection.remove(query, multi=multi)
        self.logger.info("--->数据总条数:%d, 成功删除条数: %d" % (ret["n"], ret["ok"]))
        return ret["n"] if ret["ok"] == 1 else 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__ == '__main__':
    with MongodbManage("test", "test_api") as mongo:
        # data = [{"test1": "1234"}, {"test2": "9876"}]
        # mongo.insert(data)
        # mongo.insert(data, query={"test1": "1234"}, allow_repeat=False)
        ret = mongo.select({"test1": "1234"}, to_list=False)
        print(ret)
        # mongo.update({"test1": "1234"}, {'$set': {'test1': 'MongoDB'}})
        # ret = mongo.delete({"test2": "qwqwqw"}, multi=True)
        # print(ret)
