#!/usr/bin/env bash
rm -f tb
scrapy runspider  --logfile=tb.log spiders/taobao.py