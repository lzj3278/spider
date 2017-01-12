#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: mysql_write_date.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2017-01-12 15:07:23
# Last Modified: 2017-01-12 17:15:26
############################

import MySQLdb
import datetime
import json


class Mysql_exec(object):

    def __init__(self, ip, username, password, database):
        self.ip = ip
        self.username = username
        self.passwd = password
        self.database = database

    def mysql_insert(self, info_dic):
        db = MySQLdb.connect(self.ip, self.username,
                             self.passwd, self.database, charset='utf8')
        cursor = db.cursor()
        json_doc = json.dumps(info_dic, ensure_ascii=False)
        title = info_dic['项目标题'].encode('utf-8')
        province = info_dic['所属省市'].encode('utf-8')
        city = info_dic['地级市(区)'].encode('utf-8')
        content = MySQLdb.escape_string(json_doc)
        release_time = info_dic['发布时间']
        created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """insert into nijian(title, province, city, content, \
            release_time, created) values ('%s','%s','%s','%s','%s','%s')""" % \
            (title, province, city, content, release_time, created)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception, e:
            print(e)
            db.rollback()
        db.close()
