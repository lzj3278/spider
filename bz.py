#!/usr/bin/python
# -*- coding:utf-8 -*-

############################
# File Name: bz.py
# Author: zhongjie.li
# email: zhongjie.li@viziner.cn
# Created Time: 2016-12-19 16:43:35
# Last Modified: 2016-12-19 17:14:56
############################

from bs4 import BeautifulSoup
html ="""
<TR>
<TD class=nijiantd1 width="16%">项目名称</TD>
<TD colSpan=5>广西崇左市扶绥县山圩镇污水处理项目</TD></TR>
<TR>
<TD class=nijiantd1>建设性质</TD>
<TD width="20%">新建</TD>
<TD class=nijiantd1 width="14%">所属省市</TD>
<TD width="18%">广西</TD>
<TD class=nijiantd1 width="14%">地级市(区)</TD>
<TD width="18%">崇左市</TD></TR>
<TR>
<TD class=nijiantd1>污水处理措施</TD>
<TD>污水处理厂</TD>
<TD class=nijiantd1>拟采工艺</TD>
<TD>暂未确定</TD>
<TD class=nijiantd1>预算投资</TD>
<TD>1500万元</TD></TR>
<TR>
<TD class=nijiantd1>计划开工时间</TD>
<TD>2017年</TD>
<TD class=nijiantd1>资金来源</TD>
<TD>PPP</TD>
<TD class=nijiantd1>资金落实</TD>
<TD>未落实</TD></TR>
<TR>
<TD class=nijiantd1>项目地址</TD>
<TD colSpan=3>广西崇左市扶绥县山圩镇</TD>
<TD class=nijiantd1>发布时间</TD>
<TD>2016年12月16日</TD></TR>
<TR>
<TD class=nijiantd1 height=50>项目进展</TD>
<TD colSpan=5>2016年12月16日项目进展情况备注：PPP招标阶段，黄工说项目前期的环评、设计都已做，由PPP单位负责后期的土建施工及设备安装。</TD></TR>
<TR>
<TD class=nijiantd1 height=67>项目简介</TD>
<TD colSpan=5>
<P>建设地址：项目位于广西崇左市扶绥县山圩镇。</P>
<P>建设内容：项目采用生物转盘法污水处理工艺，出水水质要达到《城镇污水处理厂污染物排放标准》（GB18918-2002）一级标准的A标准。建设规模为近期（2020年）处理规模1000m3/d，远期（2030年）处理规模2000m3/d，主要建设内容为近期建设日处理1000吨污水处理厂1座，配套建设污水管网7.1km。</P>
<P>项目投资：项目总投资1500万元（业主估算）。</P></TD></TR>
<TR>
<TD class=nijiantd1 height=80>业主单位联系信息</TD>
<TD colSpan=5>
<P>单位名称：扶绥县住房和城乡建设局 <BR>联系人：黄工/王学武（先生）<BR>部门：规划股<BR>电话：0771-7500252<BR>邮编：532200<BR>地址：广西崇左市扶绥县松江街2号<BR>联系人备注：负责项目前期手续及招标 </P>
<P>单位名称：扶绥县住房和城乡建设局<BR>联系人：何学荣<BR>职务：副局<BR>电话：0771-7513628<BR>电话：0771-7510588（局办公室）<BR>邮编：532200<BR>地址：广西崇左市扶绥县松江街2号<BR>联系人备注：项目总负责人</P></TD></TR></TBODY></TABLE>
"""
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
for string in soup.strings:
    print repr(string).encode('utf-8')

