# coding:utf-8

from lxml.html import etree
from json import loads, dumps
from re import compile as re_compile

from requests import get as http_get, post as http_post

from weiboSpider.data_type import HttpData
from weiboSpider.tools.utils import handle_exception

reg_blank = re_compile('\s+')


@handle_exception()
def json_to_str(text):
    """
    json转str
    :param text:
    :return:
    """
    return dumps(text)


@handle_exception()
def str_to_json(text):
    """
    str转json
    :param text:
    :return:
    """
    return loads(text)


def http_request(url, method=None, headers=None, cookies=None, data=None, timeout=None, logger=None):
    """
    封装网络请求
    :param url:
    :param method:
    :param headers:
    :param cookies:
    :param data:
    :param timeout:
    :param logger:
    :return: response or None
    """
    if logger is None:
        logger = default_logger
    try:
        if not isinstance(url, str):
            logger.error("URL格式不正确")
            return
        if not method:
            method = HttpData.HTTP_METHOD_GET
        if not headers:
            headers = HttpData.HTTP_DEFAULT_HEADERS
        if method == HttpData.HTTP_METHOD_GET:
            response = http_get(url, headers=headers, cookies=cookies, timeout=timeout, verify=False)
        elif method == HttpData.HTTP_METHOD_POST:
            if not data:
                data = {}
            response = http_post(url, headers=headers, cookies=cookies, data=data, timeout=timeout, verify=False)
        else:
            logger.debug("暂不支持该请求类型 ---> %s" % url)
            return
        if response.status_code == 200:
            logger.debug("请求成功: ---> %s" % url)
            return response
        else:
            logger.error("请求失败 code:%s , ---> %s" % (response.status_code, url))
            return
    except Exception as e:
        logger.exception("请求失败: %s ---> %s" % (url, str(e)))
        return


@handle_exception()
def xpath_match(html, xpath, get_one=True, default=None):
    """
    XPATH匹配
    :param html:
    :param xpath:
    :param get_one:
    :param default:
    :return:
    """
    if isinstance(html, str):
        dom = etree.HTML(html)
    else:
        dom = html
    res = dom.xpath(xpath)
    if res and len(res) > 0:
        if get_one:
            return res[0]
        else:
            return res
    elif default:
        return default
    else:
        return


@handle_exception()
def reg_match(page, pattern, get_one=True, default=None):
    """
    正则匹配
    :param page:
    :param pattern:
    :param get_one:
    :param default:
    :return:
    """
    if not get_one:
        res = pattern.findall(page)
    else:
        res = pattern.search(page)
        if res is not None:
            res = res.group(1)
    if res:
        return res
    elif default:
        return default
    else:
        return


@handle_exception()
def is_match(page, pattern):
    """
    是否匹配
    :param page:
    :param pattern:
    :return:
    """
    return pattern.search(page) is not None
