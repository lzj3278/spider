# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'

CONCURRENT_REQUESTS = 100
DOWNLOAD_TIMEOUT = 50
DOWNLOAD_DELAY = 0

CONCURRENT_REQUESTS_PER_DOMAIN = 16

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# SPLASH_URL = 'http://192.168.59.103:8050/'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

ITEM_PIPELINES = {
    'crawler.pipelines.CheckPipeline': 300,
    'crawler.pipelines.EncodingPipeline': 301,
    # 'crawler.pipelines.MySQLPipeline': 302,
    'crawler.pipelines.MongoPipeline': 302,
}

LOG_FILE = 'logfile'
LOG_LEVEL = 'INFO'

SPLASH_URL = 'http://127.0.0.1:8050/'

# other settings
MYSQL_HOST = '192.168.0.22'
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_DB = 'mall'

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'mall'
MONGO_COLLECTION = 'good_info'
