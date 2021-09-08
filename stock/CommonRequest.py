#!/usr/bin/python
# -*- coding: utf-8 -*-

# 发送http请求
import requests
from retry import retry
import random

main_url = "https://www.xueqiu.com"


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

# 发送雪球请求
@singleton
class XueqiuRequest(object):

    def __init__(self):
        self.cookie = ""
        self.total_count = 0
        self.random_count = random.randint(300, 400)

    @retry(requests.exceptions.ConnectionError, delay=10)
    def refresh_cookie(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
        session = requests.Session()
        response = session.get(main_url, headers=headers)
        print("response cookie: ", response.cookies.get_dict())
        cookies = []
        for item in response.cookies.items():
            cookies.append("=".join(item))
        self.cookie = ', '.join(cookies)
        self.random_count = random.randint(300, 400)

    @retry(requests.exceptions.ConnectionError, delay=10)
    def get_data(self, url):
        if self.total_count % self.random_count == 0:
            self.refresh_cookie()
            self.total_count = 0

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "close",
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        self.total_count += 1
        return response


# 发送通用请求，无需token、cookie等
@singleton
class CommonRequest(object):

    @retry(requests.exceptions.ConnectionError, delay=10)
    def get_data(self, url):
        response = requests.get(url)
        return response

