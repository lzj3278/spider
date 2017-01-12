#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: requests_seesion_demo.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-19 09:57:24
# Last Modified: 2017-01-12 17:28:57
############################

import requests
import time
import os
import re
import json
import sys
from Tools import Tool
from mysql_write_date import Mysql_exec
reload(sys)
sys.setdefaultencoding('utf-8')


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
        # os.chdir(sys.path[0])
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

    def __init__(self, username, password, category, date_stamp):
        '''
        初始化 session实例化，tool实例化
        '''
        self.c = Session_client()
        self.c.login(username, password)
        self.tool = Tool()
        self.category = category
        self.date_time = date_stamp
        self.mydb = Mysql_exec('localhost', 'root', 'lzj3278', 'aite')

    def get_nijian_link(self, pattern, sul, full_links):
        links = re.findall(pattern, sul.content)
        for i in links:
            if i[2] == self.date_time:
                full_links.append(i)
        return full_links

    def get_zhaobiao_link(self, pattern, sul, full_links):
        links = re.findall(pattern, sul.content)
        for i in links:
            if i[1] == self.date_time:
                full_links.append(base_url + i[0])
        return full_links

    def get_full_url(self, yema=6):
        '''
        抓取页面所有需要的url
        '''
        full_links = []
        home_url = "http://www.dowater.com/%s/Index.asp?page=" % (
            self.category)
        for i in range(yema):
            home_url_2 = home_url + '%s' % (i)
            sul = self.c.open(home_url_2)
            if self.category == 'nijian':
                # pattern = re.compile(
                    # r'<li
                    # class="listlink_nijian">.*?href="(/nijian/(.*?)/[^"]*)".*?</li>',
                    # re.S)
                pattern = re.compile(
                    r'<li class="listlink_nijian"><a title="([^"]*?)".*?href="(/nijian/(.*?)/[^"]*)".*?</li><li class="listclass_nijian">([^<]*)</li><li class="listdatetime_nijian">([^<]*)</li>', re.S)

                full_links = self.get_nijian_link(pattern, sul, full_links)

            elif self.category == 'zhaobiao':
                pattern = re.compile(
                    r'<li class="listlink">.*?href="(/zhaobiao/(.*?)/[^"]*)".*?</li>', re.S)
                full_links = self.get_zhaobiao_link(pattern, sul, full_links)
        return full_links

    def save_nijian_mess(self, title, info_dic):
        '''
        以json形式保存信息
        '''
        try:
            with open(new_path + '/' + title + '.txt', 'wb') as f:
                jsonObj = json.dumps(info_dic, ensure_ascii=False)
                f.write(jsonObj)
        except Exception, e:
            print e

    def get_nijian_mess(self, url_dic):
        '''
        抓取有用信息
        '''
        patterns_3 = re.compile(
            r'<TD class=[^>]*>(.*?)</TD>.*?<TD[^>]*>(.*?)</TD>', re.S)
        for item in url_dic:
            try:
                url_nijian = base_url + item[1]
                html1 = self.c.open(url_nijian)
                content_2 = html1.content.decode('gb2312').encode('utf-8')
                info_dic = {}
                info = re.findall(patterns_3, content_2)
                title = self.tool.replace(item[0]).decode(
                    'gb2312').encode('utf-8')
                for i in info:
                    new_item = self.tool.replace(i[1])
                    info_dic[i[0]] = new_item
                info_dic['项目状态'] = item[-2].decode('gb2312').encode('utf-8')
                info_dic['发布时间'] = item[-1]
                info_dic['项目标题'] = title
                # self.save_nijian_mess(title, info_dic)
                self.mydb.mysql_insert(info_dic)
            except Exception, e:
                print(url_nijian)
                print e

    def get_zhaobiao_mes(self, url_dic):
        base_down_url = "http://www.dowater.com/member/ArticleDown.asp?Articleid="

        for item in url_dic:
            try:
                html = self.c.open(item)
                pattern = re.compile(
                    r'<div id="main_content".*?<h1>(.*?)</h1>', re.S)
                title = re.search(pattern, html.content).group(
                    1).decode('gb2312').encode('utf-8')
                item = item[-10:-4]
                down_url = base_down_url + item
                r = self.c.open(down_url)
                r = self.tool.replace_charset(r.content)
                with open(new_path + '/' + title + '.html', 'wb') as f:
                    f.write(r.decode('gb2312').encode('utf-8'))

            except Exception, e:
                print e


if __name__ == "__main__":
    category = sys.argv[1]
    base_url = "http://www.dowater.com/"
    date_stamp = time.strftime('%Y-%m-%d')
    # date_stamp = '2017-01-06'
    path = os.getcwd()
    # path = "/var/www/html/aiteManagement/download/"
    new_path = os.path.join(path, category, date_stamp)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    try:
        g = Get_info("artronics", "hayi", category, date_stamp)
    except Exception:
        print('登录失败，重新验证用户密码')
    else:
        dic = g.get_full_url(4)
        if category == 'nijian':
            g.get_nijian_mess(dic)
        else:
            g.get_zhaobiao_mes(dic)
