# -*- coding:utf-8 -*-
import requests
import re
import time
from collections import OrderedDict
import json
import io

from selenium import webdriver
from selenium.webdriver.support.ui import Select

citys = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県',
        '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県',
        '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県', ]
city = ['北海道', '青森県']

dics = OrderedDict()

driver = webdriver.Firefox()
driver.get('https://www.joysound.com/web/shop/list')
for city in citys:
    s1 = Select(driver.find_element_by_name('prefCd'))
    s1.select_by_visible_text(city)
    time.sleep(1)
    s2 = Select(driver.find_element_by_name('cityCd'))
    s2.select_by_value("2")
    html = driver.page_source
    pattern = re.compile(r'<select.*?name="cityCd"(.*?)</select>', re.S)
    html2 = re.findall(pattern, html)
    pattern1 = re.compile(r'<option.*?>(.*?)</option>', re.S)
    result = re.findall(pattern1, html2[0])[1:]
    dics[city] = result

with open('japan_city.json', "wb") as f:
    file = json.dumps(dics, ensure_ascii=False).encode('utf8')
    f.write(file)
