# coding:utf-8
import logging
from json import loads, dumps
from functools import wraps

from requests import get as http_get, post as http_post

from weiboSpider.data_type import HttpData

default_logger = logging.getLogger(__name__)


def handle_exception(logger=None, default_val=None, show_error=True):
    """
    处理异常装饰器
    :param logger:
    :param default_val:
    :param show_error:
    :return:
    """
    if not logger:
        logger = default_logger

    def _handle(func):
        @wraps(func)
        def __handle(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if default_logger is not None:
                    logger.info("执行函数[%s]出错,返回默认值" % func.__name__)
                    return default_val
                err_msg = "执行函数{func}出错:{error}"
                error = ""
                if show_error:
                    error = str(e)
                err_msg = err_msg.format(func=func.__name__, error=error)
                logger.exception(err_msg)
        return __handle
    return _handle


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
        response = None
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
