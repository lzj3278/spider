#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: requests_seesion_demo.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-19 09:57:24
# Last Modified: 2017-01-06 17:19:24
############################

import requests
import time
import os
import re
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

home_url = "http://www.dowater.com/nijian/"
base_url = "http://www.dowater.com/"
date_stamp = time.strftime('%Y-%m-%d')
path = os.getcwd()
new_path = os.path.join(path, '拟建项目', date_stamp)
if not os.path.isdir(new_path):
    os.makedirs(new_path)


class Tool:
    '''
    去除多余符号
    '''
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<P.*?>|</P>')
    replaceBR = re.compile('<BR><BR>|<BR>')
    removeAddr = re.compile('<A.*?>|</A>')
    removeFont = re.compile('<FONT.*?>|</FONT>')
    # removeImg = re.compile('<img.*?>| {7}|')
    removeExtraTag = re.compile('\r|\n')

    def replace(self, x):
        x = re.sub(self.replaceTD, " ", x)
        x = re.sub(self.replacePara, " ", x)
        x = re.sub(self.replaceBR, " ", x)
        # x = re.sub(self.removeImg, " ", x)
        x = re.sub(self.removeFont, " ", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeExtraTag, " ", x)
        return x.strip()


class Session_client(object):
    '''
    requests 连接类
    '''
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
        '''
        登陆方法，通过返回页面中的用户来确定是否登录成功
        '''
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

    def open(self, url, delay=0, timeout=10):
        '''
        requests 打开url方法
        '''
        if delay:
            time.sleep(delay)
        return self._session.get(url, timeout=timeout)


class Get_info(object):
    '''
    抓取信息类
    '''

    def __init__(self, username, password):
        '''
        初始化 session实例化，tool实例化
        '''
        self.c = Session_client()
        self.c.login(username, password)
        self.tool = Tool()

    def get_full_url(self, home_url):
        '''
        抓取页面所有需要的url
        '''
        sul = self.c.open(home_url)
        # print(sul.content.decode('gb2312').encode('utf-8'))
        pattern = re.compile(
            r'<li class="listlink_nijian">.*?href="(/nijian/(.*?)/[^"]*)".*?</li>', re.S)
        links = re.findall(pattern, sul.content)
        full_links = []
        for i in links:
            if i[1] == date_stamp:
                full_links.append(base_url + i[0])
        return full_links

    def save_mess(self, title, info_dic):
        '''
        以json形式保存信息
        '''
        try:
            with open(new_path + '/' + title + '.txt', 'wb') as f:
                jsonObj = json.dumps(info_dic, ensure_ascii=False)
                f.write(jsonObj)
        except Exception, e:
            print e

    def get_mess(self, url_dic):
        '''
        抓取有用信息
        '''
        patterns_3 = re.compile(
            r'<TD class=[^>]*>(.*?)</TD>.*?<TD[^>]*>(.*?)</TD>', re.S)
        for item in url_dic:
            try:
                html1 = self.c.open(item)
                content_2 = html1.content.decode('gb2312').encode('utf-8')
                info_dic = {}
                info = re.findall(patterns_3, content_2)
                title = info[0][1]
                for i in info:
                    new_item = self.tool.replace(i[1])
                    info_dic[i[0]] = new_item
                self.save_mess(title, info_dic)
            except Exception:
                print('编码错误')


if __name__ == "__main__":
    try:
        g = Get_info("artronics", "hayi")
    except Exception:
        print('登录失败，重新验证用户密码')
    else:
        dic = g.get_full_url(home_url)
        g.get_mess(dic)
