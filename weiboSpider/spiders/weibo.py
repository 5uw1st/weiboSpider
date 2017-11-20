# coding:utf-8
from scrapy import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule


class WeiboSpider(CrawlSpider):
    """
    微博爬虫
    """

    name = "weibo_spider"
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/login.php']

    rules = (
        Rule(LinkExtractor(allow=('category\.php',), deny=('subsection\.php',))),

        Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    )

    def __init__(self, *args, **kwargs):
        super(WeiboSpider).__init__(*args, **kwargs)

    def start_requests(self):
        return [Request("http://www.zhihu.com/#signin", meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        pass


