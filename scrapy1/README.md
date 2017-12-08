使用 Scrapy + Scrapy_Splash 爬取京东、天猫、淘宝等网站的信息

## 项目依赖

1. Scrapy == 1.0.4
2. Scrapy_Splash
3. MySQLdb (要求 MySQL)/ PyMongo (要求 MongoDB)

## 运行步骤

1. 启动 Splash

```
sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash
```

2. 运行 run*.sh 运行爬虫
