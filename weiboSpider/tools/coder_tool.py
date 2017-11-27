# coding:utf-8

from base64 import b64decode, b64encode
from urllib.parse import quote, unquote

from weiboSpider.tools.utils import handle_exception


@handle_exception()
def enb64(text):
    if isinstance(text, str):
        text = text.encode()
    return b64encode(text)


@handle_exception()
def deb64(text):
    if isinstance(text, str):
        text = text.encode()
    return b64decode(text)


@handle_exception()
def url_encode(text):
    if isinstance(text, str):
        text = text.encode()
    return quote(text)


@handle_exception()
def url_decode(text):
    if isinstance(text, str):
        text = text.encode()
    return unquote(text)
