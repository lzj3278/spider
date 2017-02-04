#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: requests_seesion_demo.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-19 09:57:24
# Last Modified: 2017-02-04 14:10:52
############################

import time
import os
import re
import json
import sys
from collections import OrderedDict
from Tools import Tool
from mysql_write_date import Mysql_exec
from session_client import Session_client
reload(sys)
sys.setdefaultencoding('utf-8')


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

    def get_link(self, pattern, sul, full_links):
        """
        获取包含所需信息的字典
        """
        links = re.findall(pattern, sul.content)
        for i in links:
            if i[2] == self.date_time:
                full_links.append(i)
        return full_links

    # def get_zhaobiao_link(self, pattern, sul, full_links):
        # links = re.findall(pattern, sul.contenti)
        # for i in links:
        # if i[1] == self.date_time:
        # full_links.append(i)
        # return full_links

    def get_full_url(self, yema=6):
        '''
        抓取页面所有需要的url
        '''
        home_url = "http://www.dowater.com/%s/Index.asp?page=" % (
            self.category)
        full_links = []
        for i in range(1, yema):
            home_url_2 = home_url + '%s' % (i)
            sul = self.c.open(home_url_2)
            if self.category == 'nijian':
                pattern = re.compile(
                    r'<li class="listlink_nijian"><a title="([^"]*?)".*?href="(/nijian/(.*?)/[^"]*)".*?</li><li class="listclass_nijian">([^<]*)</li><li class="listdatetime_nijian">([^<]*)</li>', re.S)
                full_links = self.get_link(pattern, sul, full_links)
            elif self.category == 'zhaobiao':
                pattern = re.compile(
                    r'<li class="listlink"><a title="([^"]*?)".*?href="(/zhaobiao/(.*?)/[^"]*)".*?</li>.*?<li class="listdatetime">([^<]*)</li>', re.S)
                full_links = self.get_link(pattern, sul, full_links)
            elif self.category == 'zhongbiao':
                pattern = re.compile(
                    r'<li class="listlink"><a title="([^"]*?)".*?href="(/zhongbiao/(.*?)/[^"]*)".*?</li>.*?<li class="listdatetime">([^<]*)</li>', re.S)
                full_links = self.get_link(pattern, sul, full_links)
            elif self.category == 'shenpi':
                pattern = re.compile(
                    r'<li class="listlink"><a title="([^"]*?)".*?href="(/shenpi/(.*?)/[^"]*)".*?</li>.*?<li class="listdatetime">([^<]*)</li>', re.S)
                full_links = self.get_link(pattern, sul, full_links)

        return full_links

    def save_nijian_mess(self, title, info_dic):
        '''
        以json形式保存拟建信息
        '''
        try:
            with open(new_path + '/' + title + '.txt', 'wb') as f:
                jsonObj = json.dumps(info_dic, ensure_ascii=False)
                f.write(jsonObj)
        except Exception, e:
            print e

    def get_nijian_mess(self, url_dic):
        '''
        抓取拟建信息
        '''
        patterns_3 = re.compile(
            r'<TD class=[^>]*>(.*?)</TD>.*?<TD[^>]*>(.*?)</TD>', re.S)
        for item in url_dic:
            try:
                url_nijian = base_url + item[1]
                html1 = self.c.open(url_nijian)
                content_2 = html1.content.decode(decode_str).encode('utf-8')
                # info_dic = {}
                info_dic = OrderedDict()
                info = re.findall(patterns_3, content_2)
                title = self.tool.replace(item[0]).decode(
                    decode_str).encode('utf-8')
                for i in info:
                    new_item = self.tool.replace(i[1])
                    info_dic[i[0]] = new_item
                info_dic['项目状态'] = item[-2].decode(decode_str).encode('utf-8')
                info_dic['发布时间'] = item[-1]
                info_dic['项目标题'] = title
                # self.save_nijian_mess(title, info_dic)
                self.mydb.mysql_nijian_insert(info_dic)
            except Exception, e:
                print(url_nijian)
                print e

    def get_other_mes(self, url_dic):
        """
        下载招标，中标，审批信息
        """
        base_down_url = "http://www.dowater.com/member/ArticleDown.asp?Articleid="

        for item in url_dic:
            try:
                # pattern = re.compile(
                    # r'<div id="main_content".*?<h1>(.*?)</h1>', re.S)
                # title = re.search(pattern, html.content).group(
                    # 1).decode(decode_str).encode('utf-8')
                title = item[0].decode(decode_str).encode('utf-8')
                info_dic = OrderedDict()
                info_dic['title'] = item[0].decode(decode_str).encode('utf-8')
                info_dic['release'] = item[-1]
                info_dic['content'] = title + '.html'
                info_dic['category'] = self.category
                item = item[1][-10:-4]
                down_url = base_down_url + item
                r = self.c.open(down_url)
                r = self.tool.replace_charset(r.content)
                r = self.tool.remove_unuse(r.decode(decode_str).encode('utf-8'))
                with open(new_path + '/' + title + '.html', 'wb') as f:
                    f.write(r)
                self.mydb.mysql_other_insert(info_dic)

            except Exception, e:
                print e


if __name__ == "__main__":
    category = sys.argv[1]
    decode_str = 'gb18030'
    base_url = "http://www.dowater.com/"
    date_stamp = time.strftime('%Y-%m-%d')
    # path = os.getcwd()
    path = "/var/www/html/aiteManagement/download/"
    new_path = os.path.join(path, category, date_stamp)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    try:
        g = Get_info("artroni", "hayi", category, date_stamp)
    except Exception:
        print('登录失败，重新验证用户密码')
    else:
        dic = g.get_full_url(4)
        if category == 'nijian':
            g.get_nijian_mess(dic)
        elif category == 'zhaobiao':
            g.get_other_mes(dic)
        elif category == 'zhongbiao':
            g.get_other_mes(dic)
        elif category == 'shenpi':
            g.get_other_mes(dic)
