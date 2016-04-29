#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import re

import os, sys, urllib2, time, random,urllib

path = os.getcwd()
new_path = os.path.join(path, u'漫画')

if not os.path.isdir(new_path):
	os.mkdir(new_path)


def find_img():
	url = 'http://manhua.fhxxw.cn/comic/2121/163935_2.html'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	request = urllib2.Request(url,headers = headers)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	my_page1 = soup.prettify()
	# my_page = soup.find_all('img')
	# my_page1 = soup.find_all(src=re.compile("2121"))
	print my_page1



find_img()
