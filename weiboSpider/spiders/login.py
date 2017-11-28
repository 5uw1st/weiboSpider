# coding:utf-8

from time import time
from re import compile as re_compile

from requests import session

from weiboSpider.data_type import HttpData
from weiboSpider.spiders.utils import http_request, str_to_json, json_to_str, reg_match, is_match
from weiboSpider.tools.coder_tool import enb64, url_encode
from weiboSpider.tools.rsa_tool import RsaUtil
from weiboSpider.tools.utils import handle_exception, default_logger, Singleton


class WeiboLogin(Singleton):
    """
    微博登录
    """

    def __init__(self):
        self.logger = default_logger
        self.headers = HttpData.HTTP_DEFAULT_HEADERS
        self._timeout = HttpData.HTTP_TIME_OUT
        self._succ_status_code = 200
        self.headers.update({"Host": "login.sina.com.cn"})
        self.cookies = None
        self.__cookies_file = "cookies.txt"
        self._index_url = "https://weibo.com/login.php"
        self.__login_post_url = "https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"
        self.__get_param_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=&rsakt=mod"
        self.reg_location_url = re_compile(r'location\.replace\([\'"](.*?)[\'"]\)')
        self.reg_uuid_pa = re_compile(r'"uniqueid":"(.*?)"')
        self.reg_get_arrurl = re_compile(r',"arrURL":\["([\s\S]+?)"\]')
        self.reg_location = re_compile(r'/u/\d+?/home\?wvr=\d+')

    @handle_exception(default_val=False)
    def login(self, username, password):
        """
        登录接口
        :param username:
        :param password:
        :return:
        """
        # 首先尝试cookies登录，失败再账号登录
        isSucc = self.__cookies_login()
        if not isSucc:
            self.logger.debug("<---cookies登录失败,尝试账号登录中...")
            isSucc = self.__account_login(username, password)
            if isSucc:
                self.logger.info("--->账号登录成功")
                return True
            else:
                self.logger.debug("<---账号登录失败")
                return False
        else:
            self.logger.info("--->cookies登录成功")
            return True

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
                    for url in arr_urls:
                        js_url = url.replace("\\", "").replace('"', "")
                        tmp = http_session.get(js_url, headers=self.headers, verify=False).text
                    location_url = reg_match(text, self.reg_location_url)
                    text = http_session.get(location_url, verify=False).content.decode("gb18030")
                    uuid_res = reg_match(text, self.reg_uuid_pa)
                    self.logger.info("登录成功:uuid --> %s" % uuid_res)
                    cookies = http_session.cookies.get_dict()
                    res = http_session.get("https://weibo.com/")
                    if self.__judge_login_status(cookies_dict=cookies):
                        self.logger.info("登录成功")
                        self.__save_cookies(cookies)
                        return True
                self.logger.debug("登录失败: ---> %d" % response.status_code)
            return False
        except Exception as e:
            self.logger.exception("登录失败: %s ---> %s" % (username, str(e)))
            return False

    def __judge_login_status(self, cookies_dict):
        """
        判断登录状态
        :param cookies_dict:
        :return:
        """
        base_url = "https://weibo.com/"
        my_headers = self.headers.copy()
        my_headers.update({
            "Host": "weibo.com",
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Accept-Language": "zh-CN,zh;q=0.8",
        })
        response = http_request(base_url, headers=my_headers, cookies=cookies_dict, logger=self.logger)
        current_url = response.url
        if is_match(current_url, self.reg_location):
            self.logger.info("登录状态为登录成功")
            self.cookies = cookies_dict
            return True
        self.logger.info("登录状态为登录失败")
        return False

    def __save_cookies(self, cookies_dict):
        """
        保存cookies到文件
        :param cookies_dict:
        :return:
        """
        with open(self.__cookies_file, "w") as cf:
            cookies_data = json_to_str(cookies_dict)
            cf.write(cookies_data)
            return True

    def __read_cookies(self):
        """
        从文件中读取cookies
        :return:
        """
        try:
            with open(self.__cookies_file, "r") as cf:
                return str_to_json(cf.read())
        except Exception as e:
            self.logger.exception("读取cookies出错:%s" % str(e))
            return

    def __cookies_login(self):
        """
        cookies登录
        :return:
        """
        cookies_data = self.__read_cookies()
        if cookies_data:
            if self.__judge_login_status(cookies_dict=cookies_data):
                self.logger.info("cookies登录成功")
                return True
        self.logger.info("cookies登录失败")
        return False

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
    print(issucc, t.cookies)
