# coding:utf-8

from weiboSpider.items import UserInfoItem, BlogInfoItem, CommentInfoItem, \
    ShareInfoItem, FollowInfoItem, FanInfoItem
from weiboSpider.spiders.base import BaseSpider


class WeiboSpider(BaseSpider):
    """
    微博爬虫
    """

    name = "weibo_spider"
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/login.php']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_user_info(self, response):
        """
        解析用户信息
        :param response:
        :return:
        """
        item = UserInfoItem()
        item["uid"] = ""
        yield item

    def parse_blog_info(self, response):
        """
        解析微博信息
        :param response:
        :return:
        """
        pass
