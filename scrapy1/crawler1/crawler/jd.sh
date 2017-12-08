#!/usr/bin/env bash
rm -f jd
scrapy runspider  --logfile=jd.log spiders/jd.py