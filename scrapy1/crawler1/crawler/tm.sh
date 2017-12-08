#!/usr/bin/env bash
rm -f tm
scrapy runspider  --logfile=tm.log spiders/tm.py