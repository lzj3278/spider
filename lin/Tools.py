#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: Tools.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2017-01-12 08:59:42
# Last Modified: 2017-01-17 13:56:46
############################

import re


class Tool:
    '''
    去除多余符号,以及不需要的数据
    '''
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<P.*?>|</P>')
    # replaceBR = re.compile('<BR><BR>|<BR>')
    removeAddr = re.compile('<A.*?>|</A>')
    removeFont = re.compile('<FONT.*?>|</FONT>')
    removefont = re.compile('<font.*?>|</font>')
    # removeImg = re.compile('<img.*?>| {7}|')
    removeExtraTag = re.compile('\r|\n')
    removecharset = re.compile('gb2312')
    removeSpan = re.compile('<SPAN[^>]*?>|</SPAN>')
    removespace = re.compile('&nbsp;')
    removecenter = re.compile('<center><img.*?</center>')
    removecenter2 = re.compile('<font color="#999999".*?</font>', re.S)
    removeinfo = re.compile('数据来源：中国污水处理工程网', re.S)

    def replace_charset(self, x):
        x = re.sub(self.removecharset, "utf-8", x)
        return x.strip()

    def remove_unuse(self, x):
        x = re.sub(self.removecenter, "", x)
        x = re.sub(self.removecenter2, "", x)
        x = re.sub(self.removeinfo, "", x)
        return x.strip()

    def replace(self, x):
        x = re.sub(self.replaceTD, " ", x)
        x = re.sub(self.replacePara, " ", x)
        # x = re.sub(self.replaceBR, " ", x)
        # x = re.sub(self.removeImg, " ", x)
        x = re.sub(self.removeFont, " ", x)
        x = re.sub(self.removefont, " ", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeExtraTag, " ", x)
        x = re.sub(self.removeSpan, "", x)
        x = re.sub(self.removespace, "", x)
        return x.strip()
