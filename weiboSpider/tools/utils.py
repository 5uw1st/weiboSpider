# coding:utf-8

import logging
from functools import wraps
from time import time

default_logger = logging.getLogger(__name__)


class Singleton(object):
    """
    单例模式类
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


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


def get_timestamp(default_type=True):
    """
    获取时间戳
    :param default_type: 10位或者13位
    :return:
    """
    if default_type:
        return str(int(time()))
    else:
        return str(int(time())*1000)


def trim_all(text, opt_list=None):
    """
    去除空格换行等字符
    :param text:
    :param opt_list:
    :return:
    """
    try:
        if not isinstance(text, str):
            return None
        res = ""
        default_list = ["\n", "\r\n", "\t", "&nbsp;", "\xa0"]
        if opt_list is not None and isinstance(opt_list, list):
            default_list += opt_list
        for i in set(default_list):
            res = text.replace(i, "")
        res = reg_blank.sub('', res)
        res = res.strip()
        return res
    except Exception as e:
        return text