#!/usr/bin/env python
# coding: utf-8

import Queue
import os
import threading
import urllib2
import re

from bs4 import BeautifulSoup

path = os.getcwd()
new_path = os.path.join(path, u'漫画')
if not os.path.isdir(new_path):
	os.mkdir(new_path)
q = Queue.Queue(0)
# url_base = 'http://www.veerchina.com'
url = 'https://alpha.wallhaven.cc/random'


def find_img(url):
	url1 = url
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent': user_agent}
	request = urllib2.Request(url1, headers=headers)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	my_page = soup.find_all('a')
	pic_url = []
	for item in my_page:
		pic_url.append(item.get('href'))
	# print pic_url
	return pic_url


def head_url(url1):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent': user_agent}
	request = urllib2.Request(url1, headers=headers)
	response = urllib2.urlopen(request)
	return response


def find_img_2(url):
	url1 = url
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent': user_agent}
	request = urllib2.Request(url1, headers=headers)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	my_page = soup.find_all('img')
	pic_url = []
	for item in my_page:
		pic_url.append(item.get('src'))
	# print pic_url
	return pic_url


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


if __name__ == '__main__':
	print 'begin'
	full_url_dic = get_full_url()
	for i in full_url_dic:
		q.put(i)
	print "job qsize:", q.qsize()
	while True:
		my_thread = Mythread(get_picture, q.get())
		my_thread.start()
		# my_thread.join()
		print q.qsize()
		if q.qsize() == 0:
			break
