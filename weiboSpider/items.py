# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BaseInfoItem(Item):
    """
    BaseItem
    """
    uid = Field()


class UserInfoItem(Item):
    """
    微博个人信息
    """
    uid = Field()
    username = Field()
    photo = Field()
    sex = Field()
    member_level = Field()
    desc = Field()
    follows = Field()
    fans = Field()
    blogs = Field()
    nickname = Field()
    province = Field()
    city = Field()
    birthday = Field()
    blog_address = Field()
    reg_time = Field()
    education = Field()  # [{},{},...]
    # {
    #     "school": "",
    #     "class": "",
    #     "academy": "",
    # }
    tags = Field  # []
    level = Field()
    credit_level = Field()


class BlogInfoItem(Item):
    """
    微博详细信息
    """
    uid = Field()
    bid = Field()
    time = Field()
    send_from = Field()
    content = Field()
    share = Field()
    comment = Field()
    thumb_up = Field()


class CommentInfoItem(Item):
    """
    微博评论信息
    """
    uid = Field()
    bid = Field()
    cid = Field()
    c_name = Field()
    c_uid = Field()
    c_msg = Field()
    c_time = Field()
    c_thumb_up = Field()


class ShareInfoItem(Item):
    """
    微博分享信息
    """
    uid = Field()
    bid = Field()
    sid = Field()
    s_name = Field()
    s_uid = Field()
    s_msg = Field()
    s_time = Field()
    s_thumb_up = Field()


class FollowInfoItem(Item):
    """
    关注人信息
    """
    uid = Field()
    fid = Field()
    f_name = Field()
    f_uid = Field()
    f_from = Field()


class FanInfoItem(Item):
    """
    粉丝信息
    """
    uid = Field()
    fanid = Field()
    fan_name = Field()
    fan_uid = Field()
    fan_from = Field()
