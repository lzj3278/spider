#!/usr/bin/env python
# coding: utf-8

import Queue
import os
import threading
import urllib2

from bs4 import BeautifulSoup

path = os.getcwd()
new_path = os.path.join(path, u'漫画')
if not os.path.isdir(new_path):
	os.mkdir(new_path)
q = Queue.Queue(0)
url_base = 'http://www.veerchina.com'


def find_img():
	url = 'http://www.veerchina.com/q/摩托车/'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = {'User-Agent': user_agent}
	request = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	my_page = soup.find_all('img')
	pic_url = []
	for item in my_page:
		pic_url.append(item.get('data-original'))
	return pic_url


def filter_url(url):
	if url is not None:
		return url


def get_full_url():
	result = filter(filter_url, find_img())
	full_url = []
	for item in result:
		full_url.append(url_base + item)
	# print full_url
	return full_url


class Mythread(threading.Thread):
	def __init__(self, target, args):
		super(Mythread, self).__init__()
		self.target = target
		self.args = args

	def run(self):
		self.target(self.args)


def get_picture(url):
	contents = urllib2.urlopen(url).read()
	with open(u'漫画' + '/' + url[-11:], 'wb') as f:
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
		my_thread.join()
		print q.qsize()
		if q.qsize() == 0:
			break
