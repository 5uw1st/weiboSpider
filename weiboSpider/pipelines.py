# -*- coding: utf-8 -*-

from weiboSpider.database.db_setting import MongodbName, MongodbTable
from weiboSpider.database.mongodb import MongodbManage
from weiboSpider.items import UserInfoItem, BlogInfoItem, CommentInfoItem, \
    ShareInfoItem, FollowInfoItem, FanInfoItem
from weiboSpider.tools.utils import trim_all


class WeibospiderPipeline(object):
    db_name = MongodbName.MONGODB_WEIBO_DB

    def process_item(self, item, spider):
        data = {}
        for k, v in item.items():
            data[k] = self.trim_field(v)

        if isinstance(item, UserInfoItem):
            collection_name = MongodbTable.MONGODB_USER_INFO
            query_dic = {"uid": data.get("uid", "")}
            self.write_in_mongodb(data, self.db_name, collection_name, query_dic)
        elif isinstance(item, BlogInfoItem):
            collection_name = MongodbTable.MONGODB_BLOG_INFO
            query_dic = {"uid": data.get("uid", ""), "bid": data.get("bid", "")}
            self.write_in_mongodb(data, self.db_name, collection_name, query_dic)
        elif isinstance(item, CommentInfoItem):
            collection_name = MongodbTable.MONGODB_COMMENT_INFO
            query_dic = {"uid": data.get("uid", ""), "cid": data.get("cid", "")}
            self.write_in_mongodb(data, self.db_name, collection_name, query_dic)
        elif isinstance(item, ShareInfoItem):
            collection_name = MongodbTable.MONGODB_SHARE_INFO
            query_dic = {"uid": data.get("uid", ""), "sid": data.get("sid", "")}
            self.write_in_mongodb(data, self.db_name, collection_name, query_dic)
        elif isinstance(item, FollowInfoItem):
            collection_name = MongodbTable.MONGODB_FAN_INFO
            query_dic = {"uid": data.get("uid", ""), "folid": data.get("folid", "")}
            self.write_in_mongodb(data, self.db_name, collection_name, query_dic)
        elif isinstance(item, FanInfoItem):
            collection_name = MongodbTable.MONGODB_FAN_INFO
            query_dic = {"uid": data.get("uid", ""), "fanid": data.get("fanid", "")}
            self.write_in_mongodb(data, self.db_name, collection_name, query_dic)
        else:
            return item

    def write_in_mongodb(self, data, db_name, collect_name, query_dict):
        """
        将数据保存至mongodb
        :param data:
        :param db_name:
        :param collect_name:
        :param query_dict:
        :return:
        """
        with MongodbManage(db_name=db_name, collection=collect_name) as mongo:
            insert_id = mongo.insert(data=data, query=query_dict, allow_repeat=False)
        return insert_id

    def trim_field(self, field):
        """
        去除字段多余字符
        :param field:
        :return:
        """
        if isinstance(field, list):
            result = [trim_all(i) for i in field]
        elif isinstance(field, None):
            result = ""
        elif isinstance(field, str):
            result = trim_all(field)
        else:
            result = field
        return result
