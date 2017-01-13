#!/usr/bin/env python
# coding: utf-8

import threading
from time import ctime, sleep

loops = [4, 2]


def loop(nloop, nsec):
	print 'start loop', nloop, 'at:', ctime()
	sleep(nsec)
	print 'loop', nloop, 'at:', ctime()


def main():
	print 'starting at:', ctime()
	thread = []
	nloops = range(len(loops))
	for i in nloops:
		t = threading.Thread(target=loop, args=(i, loops[i]))
		thread.append(t)
	for i in nloops:
		thread[i].start()
	for i in nloops:
		thread[i].join()
	print 'all done at:', ctime()


if __name__ == '__main__':
	main()
