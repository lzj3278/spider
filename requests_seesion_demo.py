#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: requests_seesion_demo.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-19 09:57:24
# Last Modified: 2016-12-19 17:35:26
############################

import requests
import time
import os
import re
import sys
from bs4 import BeautifulSoup as BS
reload(sys)
sys.setdefaultencoding('utf-8')

home_url = "http://www.dowater.com/nijian/"
base_url = "http://www.dowater.com/"


class Session_client(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.dowater.com",
        "Upgrade-Insecure-Requests": "1",
    }
    loginURL = "http://www.dowater.com/login/login1.asp"

    def __init__(self):
        os.chdir(sys.path[0])
        self._session = requests.Session()
        self._session.headers = self.headers

    def login(self, username, password):
        self._username = username
        self._password = password
        self._loginurl = self.loginURL
        while True:
            data = {
                "UsernameGet": self._username,
                "passwordget": self._password,
                "yixiang_Action": 'yixiang_Add',
                "Verifycode": 8888,
                "submit2": '',
            }
            res = self._session.post(self._loginurl, data=data)
            content = res.text
            name_pat = re.compile(
                r'<a\b[^>]*class="headlink"[^>]*>(.*?)</a>', re.S)
            name_find = re.search(name_pat, content)
            if name_find.group(1) == self._username:
                print("登陆成功")
                break
            else:
                print("登录失败，重新输入")

    def open(self, url, delay=0, timeout=10):
        if delay:
            time.sleep(delay)
        return self._session.get(url, timeout=timeout)


class Get_info(object):

    def __init__(self, username, password):
        self.c = Session_client()
        self.c.login(username, password)

    def get_full_url(self, home_url):
        sul = self.c.open(home_url)
        print(sul.content.decode('gb2312').encode('utf-8'))
        pattern = re.compile(
            r'<li class="listlink_nijian">.*?href="([^"]*)".*?</li>', re.S)
        links = re.findall(pattern, sul.content)
        full_links = []
        for i in links:
            full_links.append(base_url + i)
        return full_links

    def get_mess(self, url_dic):
        patterns_2 = re.compile(
            r'<TD class=nijiantd[^>]*>(.*?)</TD>', re.S)
        patterns_3 = re.compile(
            r'<TD class=nijiantd.*?</TD>\n*<TD.*?>(.*?)</TD>', re.S)
        for item in url_dic:
            html1 = self.c.open(item)
            content_2 = html1.content.decode('gb2312').encode('utf-8')
            # print html1.content
            # print content_2
            info = re.findall(patterns_2, content_2)
            for i in info:
                print i.encode('utf-8')


if __name__ == "__main__":
    g = Get_info("artronics", "hayi2017")
    # g.get_full_url(home_url)
    url_dic = ["http://www.dowater.com/nijian/2016-12-16/516833.asp"]
    g.get_mess(url_dic)
