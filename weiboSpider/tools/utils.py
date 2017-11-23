# coding:utf-8

from time import time


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
