#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: meiju.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-08 16:30:41
# Last Modified: 2016-12-09 11:34:44
############################
import requests
import re
import sys
import threading
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class Archives(object):

    def save_links(self, url):
        try:

            data = requests.get(url, timeout=3)
            content = data.text
            # link_pat = '"(ed2k://\|file\|[^"]+?\.(S\d+)(E\d+)[^"]+?1024X\d{3}[^"]+?)"'
            link_pat = '"(ed2k://\|file\|[^"]+?\.(S\d+)(E\d+)[^"]+?)"'
            name_pat = re.compile(r'<h2 class="entry_title">(.*?)</h2>', re.S)
            links = set(re.findall(link_pat, content))
            name = re.findall(name_pat, content)
            links_dict = {}
            count = len(links)
        except Exception, e:
            print e
        for i in links:
            links_dict[int(i[1][1:3]) * 100 + int(i[2][1:3])
                       ] = i  # 把剧集按s和e提取编号
        try:
            with open('meiju' + '/' + name[0].replace('/', '_') + '.txt', 'w') as f:
                print name[0]
                for i in sorted(list(links_dict.keys())):  # 按季数+集数排序顺序写入
                    f.write(links_dict[i][0] + '\n')
            print "Get links ... ", name[0], count
        except Exception, e:
            print e

    def get_urls(self):
        try:
            for i in range(2015, 25000):
                base_url = 'http://cn163.net/archives/'
                url = base_url + str(i) + '/'
                if requests.get(url).status_code == 404:
                    continue
                else:
                    self.save_links(url)
        except Exception, e:
            print e

    def main(self):
        thread1 = threading.Thread(target=self.get_urls())
        thread1.start()
        thread1.join()
if __name__ == '__main__':
    start = time.time()
    a = Archives()
    a.main()
    end = time.time()
    print end - start
