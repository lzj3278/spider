#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: Tools.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2017-01-12 08:59:42
# Last Modified: 2017-01-12 09:04:13
############################

import re


class Tool:
    '''
    去除多余符号
    '''
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<P.*?>|</P>')
    replaceBR = re.compile('<BR><BR>|<BR>')
    removeAddr = re.compile('<A.*?>|</A>')
    removeFont = re.compile('<FONT.*?>|</FONT>')
    removefont = re.compile('<font.*?>|</font>')
    # removeImg = re.compile('<img.*?>| {7}|')
    removeExtraTag = re.compile('\r|\n')
    removecharset = re.compile('gb2312')
    removeSpan = re.compile('<SPAN[^>]*?>|</SPAN>')

    def replace_charset(self, x):
        x = re.sub(self.removecharset, "utf-8", x)
        return x

    def replace(self, x):
        x = re.sub(self.replaceTD, " ", x)
        x = re.sub(self.replacePara, " ", x)
        x = re.sub(self.replaceBR, " ", x)
        # x = re.sub(self.removeImg, " ", x)
        x = re.sub(self.removeFont, " ", x)
        x = re.sub(self.removefont, " ", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.removeExtraTag, " ", x)
        x = re.sub(self.removeSpan, "", x)
        return x.strip()
