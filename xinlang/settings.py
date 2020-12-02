# Scrapy settings for xinlang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# name
BOT_NAME = 'xinlang'

# 日志
# LOG_LEVEL = 'WARNING' # 比warning小的都不会输出出来


# 位置
SPIDER_MODULES = ['xinlang.spiders']

# 新建爬虫的位置
NEWSPIDER_MODULE = 'xinlang.spiders'


# User-Agent
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

# ROBOTSTXT_OBEY协议
# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# 最大并发请求
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# 下载延迟
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:

# 域名
#CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 代理ip
#CONCURRENT_REQUESTS_PER_IP = 16

# 默认情况cookie是开启的
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# 默认请求头
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xinlang.middlewares.XinlangSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware':None, # retry中间件
    'xinlang.middlewares.RotateUserAgentMiddleware':544,
    'xinlang.middlewares.RandomProxyMiddleware': 545,  # 修改下载优先级数字
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'xinlang.pipelines.XinlangPipeline': 300,
   'xinlang.pipelines.WeiboPipeline': 301,
   'xinlang.pipelines.WdtyPipeline': 302,
   # 'xinlang.pipelines.MongoPipline': 303,
   'xinlang.pipelines.MysqlPipeline': 304,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


COMMANDS_MODULE = 'xinlang.commands'


# 去重类
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 调度内容持久化 表示可以持久化操作
SCHEDULER_PERSIST = True

# 优先队列
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"


REDIS_URL = 'redis://127.0.0.1:6379/2'
# REDIS_URL = 'redis://39.98.126.80:6379/2'

# MONGO_URI = 'mongodb://39.98.126.80:27017'
# MONGO_URI = 'mongodb://127.0.0.1:27017'

MONGO_DB = "finance"


MYSQL_HOST = "127.0.0.1"  # 这是你mysql服务器的主机名或ip地址
MYSQL_PORT = 3306  # 这是你mysql服务器上的端口，3306，mysql就是3306，必须是数字
MYSQL_DB = "finance"  # mysql服务器上的数据库名
MYSQL_USER = "root"  # 这是你mysql数据库上的用户名
MYSQL_PASSWORD = "209243"  # 这是你mysql数据库的密码

