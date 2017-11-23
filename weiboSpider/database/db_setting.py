# coding:utf-8

# mongodb 配置信息
MONGODB_SETTING = {
    "LOCAL": {
        "host": "127.0.0.1",
        "port": 27017,
        "username": None,
        "password": None
    },
}

# redis 配置信息
REDIS_SETTING = {
    "LOCAL": {
        "host": "127.0.0.1",
        "port": "6379",
        "db": 0,
        "password": None
    },
}


class MongodbName(object):
    """
    mongodb 库配置
    """
    MONGODB_WEIBO_DB = "sina_weibo"


class MongodbTable(object):
    """
    mongodb 表配置
    """
    MONGODB_UID_INFO = "wb_uid_info"
    MONGODB_USER_INFO = "wb_user_info"
    MONGODB_BLOG_INFO = "wb_blog_info"
    MONGODB_COMMENT_INFO = "wb_comment_info"
    MONGODB_SHARE_INFO = "wb_share_info"
    MONGODB_FOLLOW_INFO = "wb_follow_info"
    MONGODB_FAN_INFO = "wb_fan_info"


class RedisTable(object):
    """
    redis 表配置
    """
    REDIS_UID_INFO = "wb_uid"   # hset(uid, stime) --> userid
    REDIS_BID_INFO = "wb_bid"   # hset(uid_bid, stime) --> userid_blogid
    REDIS_CID_INFO = "wb_cid"   # hset(uid_bid_cid, stime) --> userid_blogid_commentid
    REDIS_SID_INFO = "wb_sid"   # hset(uid_bid_sid, stime) --> userid_blogid_shareid
    REDIS_FOLID_INFO = "wb_folid"   # hset(uid_folid, stime) --> userid_followid
    REDIS_FANID_INFO = "wb_fanid"   # hset(uid_fanid, stime) --> userid_fanid


DB_TABLE_RELATION = {
    "USER_ID": {
        "MONGODB": MongodbTable.MONGODB_UID_INFO,
        "REDIS": RedisTable.REDIS_UID_INFO
    },
    "BLOG_ID": {
        "MONGODB": MongodbTable.MONGODB_BLOG_INFO,
        "REDIS": RedisTable.REDIS_BID_INFO
    },
    "COMMENT_ID": {
        "MONGODB": MongodbTable.MONGODB_COMMENT_INFO,
        "REDIS": RedisTable.REDIS_CID_INFO
    },
    "SHARE_ID": {
        "MONGODB": MongodbTable.MONGODB_SHARE_INFO,
        "REDIS": RedisTable.REDIS_SID_INFO
    },
    "FOLLOW_ID": {
        "MONGODB": MongodbTable.MONGODB_FOLLOW_INFO,
        "REDIS": RedisTable.REDIS_FOLID_INFO
    },
    "FAN_ID": {
        "MONGODB": MongodbTable.MONGODB_FAN_INFO,
        "REDIS": RedisTable.REDIS_FANID_INFO
    },
}
