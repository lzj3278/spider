#!/usr/bin/env python
# coding: utf-8

#
# import requests
# from bs4 import BeautifulSoup
#
# url = 'http://tieba.baidu.com/p/4557007321'
# html = requests.get(url)
# contents = BeautifulSoup(html.text)
#
# print contents.find(id = "article_content")
# # print html.text

import Queue
import os
import threading
import urllib2
import re
import requests
from time import ctime

from bs4 import BeautifulSoup

path = os.getcwd()
new_path = os.path.join(path, u'漫画')
if not os.path.isdir(new_path):
	os.mkdir(new_path)

# url_base = 'http://www.veerchina.com'
url = 'https://alpha.wallhaven.cc/random'


def find_img(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.text)
	my_page = soup.find_all('a')
	pic_url = []
	for item in my_page:
		pic_url.append(item.get('href'))
	# print pic_url
	return pic_url


def find_img_2(url):
	html = requests.get(url)
	soup = BeautifulSoup(html.text)
	my_page = soup.find_all('img')
	pic_url = []
	for item in my_page:
		pic_url.append(item.get('src'))
	# print pic_url
	return pic_url


def head_url(url1):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent': user_agent}
	request = urllib2.Request(url1, headers=headers)
	response = urllib2.urlopen(request)
	return response


def filter_url(url):
	if url is not None:
		# if re.match(".*\d+$", url):
		if re.match(".*wallpaper*", url) and re.match(".*\d+$", url):
			return url


def get_full_url():
	result = filter(filter_url, find_img(url))
	print result
	return result


class Mythread(threading.Thread):
	def __init__(self, target, args):
		super(Mythread, self).__init__()
		self.target = target
		self.args = args

	def run(self):
		self.target(self.args)


def get_picture(url):
	url_big = find_img_2(url)
	url_pic = 'https:' + url_big[-1]
	print url_pic

	contents = head_url(url_pic).read()
	with open(u'漫画' + '/' + url_pic[-10:], 'wb') as f:
		f.write(contents)


def main():
	print 'begin'
	full_url_dic = get_full_url()
	thread = []
	q = Queue.Queue(0)
	for item in full_url_dic:
		q.put(item)
	print "job qsize:", q.qsize()
	queue_size = range(q.qsize())
	for i in queue_size:
		my_thread = Mythread(get_picture, q.get())
		thread.append(my_thread)
	for i in queue_size:
		thread[i].start()
	for i in queue_size:
		thread[i].join()
	print 'all done at:', ctime()


if __name__ == '__main__':
	main()
