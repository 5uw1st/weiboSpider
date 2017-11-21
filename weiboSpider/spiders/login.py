# coding:utf-8

from time import time
from re import compile as re_compile

from requests import session

from weiboSpider.data_type import HttpData
from weiboSpider.spiders.utils import http_request, default_logger, str_to_json, handle_exception, reg_match
from weiboSpider.tools.coder_tool import enb64, url_encode
from weiboSpider.tools.rsa_tool import RsaUtil


class WeiboLogin(object):
    """
    微博登录
    """

    def __init__(self):
        self.logger = default_logger

        self.headers = HttpData.HTTP_DEFAULT_HEADERS
        self._timeout = HttpData.HTTP_TIME_OUT
        self._succ_status_code = 200
        self.headers.update({"Host": "login.sina.com.cn"})
        self.__cookies = None
        self._index_url = "https://weibo.com/login.php"
        self.__login_post_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        self.__get_param_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=&rsakt=mod"
        self.reg_location_url = re_compile(r'location\.replace\([\'"](.*?)[\'"]\)')
        self.reg_uuid_pa = re_compile(r'"uniqueid":"(.*?)"')
        self.reg_get_arrurl = re_compile(r',"arrURL":\["([\s\S]+?)"\]')

    @handle_exception(default_val=False)
    def login(self, username, password):
        """
        登录接口
        :param username:
        :param password:
        :return:
        """
        isSucc = self.__account_login(username, password)
        if isSucc:
            self.logger.info("登录成功")
            return True
        else:
            self.logger.debug("登录失败")
            return False

    def __account_login(self, username, password):
        """
        账号登录
        :param username:
        :param password:
        :return:
        """
        try:
            with session() as http_session:
                http_session.get(self._index_url, headers=self.headers)
                post_data = self.__ready_post_data(username, password)
                if not post_data:
                    self.logger.error("准备登录参数失败")
                    return False
                response = http_session.post(
                    self.__login_post_url,
                    headers=self.headers,
                    data=post_data,
                    verify=False,
                    timeout=self._timeout
                )
                if response.status_code == self._succ_status_code:
                    text = response.content.decode("gb18030")
                    location_url = reg_match(text, self.reg_location_url)
                    if not location_url:
                        self.logger.debug("获取跳转URL失败，登录失败")
                        return False
                    text = http_session.get(location_url, headers=self.headers, verify=False).content.decode("gb18030")
                    arr_str = reg_match(text, self.reg_get_arrurl)
                    if not arr_str:
                        self.logger.debug("获取JS失败")
                        return False
                    arr_urls = arr_str.split(",")
                    js_url = arr_urls[0].replace("\\", "").replace('"', "")
                    text = http_session.get(js_url, headers=self.headers, verify=False).text
                    uuid_res = reg_match(text, self.reg_uuid_pa)
                    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
                    weibo_page = http_session.get(web_weibo_url, headers=self.headers, verify=False)
                    self.logger.info("登录成功")
                    self.__cookies = http_session.cookies.get_dict()
                    return True
                self.logger.debug("登录失败: ---> %d" % response.status_code)
            return False
        except Exception as e:
            self.logger.exception("登录失败: %s ---> %s" % (username, str(e)))
            return False

    def __cookies_login(self):
        """
        cookies登录
        :return:
        """
        try:
            pass
        except Exception as e:
            pass

    def __get_login_param(self):
        """
        获取登录必要参数
        :return:
        """
        try:
            response = http_request(self.__get_param_url)
            if not response:
                self.logger.error("请求登录必要参数失败")
                return
            text = response.text
            ret_json = str_to_json(text)
            if not ret_json:
                self.logger.error("转换数据失败")
                return
            return ret_json
        except Exception as e:
            self.logger.exception("获取登录必要参数出错: ---> %s" % str(e))
            return

    def __ready_post_data(self, username, password):
        """
        准备登录post参数
        :return:
        """
        try:
            rsa_params = self.__get_login_param()
            if not rsa_params:
                self.logger.debug("获取加密参数失败")
                return
            # 密码为rsa加密
            my_rsa = RsaUtil(key_is_hex=True)
            pubkey = rsa_params.get("pubkey")
            servertime = rsa_params.get("servertime", "")
            nonce = rsa_params.get("servertime", "")
            message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
            encrypt_password = my_rsa.encrypt(message, pubkey=pubkey, get_hex=True)
            post_data = {
                "entry": "weibo",
                "gateway": "1",
                "from": "",
                "savestate": rsa_params.get("exectime") or 7,
                "qrcode_flag": "false",
                "useticket": "1",
                "pagerefer": "",
                "vsnf": "1",
                "su": enb64(url_encode(username)),
                "service": "miniblog",
                "servertime": servertime,
                "nonce": nonce,
                "pwencode": "rsa2",
                "rsakv": rsa_params.get("rsakv", ""),
                "sp": encrypt_password,
                "sr": "1366*768",
                "encoding": "UTF-8",
                "prelt": "44",
                "url": "https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
                "returntype": "META",
            }
            return post_data
        except Exception as e:
            self.logger.exception("准备登录post参数出错: ---> %s" % str(e))
            return

if __name__ == '__main__':
    user = "1212"
    pwd = "1212"
    t = WeiboLogin()
    issucc = t.login(user, pwd)
    print(issucc)
