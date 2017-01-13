#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: sp.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-08 14:50:14
# Last Modified: 2016-12-08 16:29:33
############################

import urllib2
from bs4 import BeautifulSoup
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

base_url = "http://cn163.net/archives/11104/"


def head_url(url1):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url1, headers=headers)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response)
    # return response
    print soup.text


def find_img_url(url):
    response = head_url(url)
    soup = BeautifulSoup(response)
    time.sleep(2)
    my_page = soup.find_all('a')
    pic_url = []
    for item in my_page:
        pic_url.append(item.get('href'))
    # return pic_url
    print pic_url
# contents = head_url(base_url).read()

# with open('a.jpg', 'wb') as f:
    # f.write(contents)

if __name__ == "__main__":
    # url = base_url
    head_url(base_url)
    # find_img_url(base_url)
