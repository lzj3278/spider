#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: xpath_1.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2017-01-13 10:42:33
# Last Modified: 2017-01-13 15:14:32
############################

from session_client import Session_client
from lxml import etree, html
# from io import Se

s = Session_client()
s.login("artronics", "hayi2017")
html1 = s.open("http://www.dowater.com//nijian/2017-01-13/523352.asp")
tree = html.fromstring(html1.content)
fixed = html.tostring(tree, pretty_print=True)
# html2 = etree.HTML(tree)
# print html2
# result = html2.xpath('//a/text()')
# print result
print tree
