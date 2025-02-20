import os

cwd = os.getcwd()

BOT_NAME = "zj_project"

SPIDER_MODULES = ["zj_project.spiders"]
NEWSPIDER_MODULE = "zj_project.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#开启访问频率限制
AUTOTHROTTLE_ENABLED = True
#设置访问开始的延迟
AUTOTHROTTLE_START_DELAY = 5
#设置访问之间的最大延迟
AUTOTHROTTLE_MAX_DELAY = 60
#设置Scrapy 并行发给每台远程服务器的请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = 3
#设置下裁之后的自动延迟
# 下载延迟时间，单位是秒，控制爬虫爬取的频率，根据你的项目调整，不要太快也不要太慢，默认是3秒，即爬一个停3秒，设置为1秒性价比较高，如果要爬取的文件较多，写零点几秒也行
DOWNLOAD_DELAY = 1
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 最大并发数，很好理解，就是同时允许开启多少个爬虫线程
CONCURRENT_REQUESTS = 4
# CONCURRENT_REQUESTS = 1


# Disable cookies (enabled by default)
# COOKIES_ENABLED：是否保存COOKIES，默认关闭，开机可以记录爬取过程中的COKIE，非常好用的一个参数
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS：默认请求头，上面写了一个USER_AGENT，其实这个东西就是放在请求头里面的，这个东西可以根据你爬取的内容做相应设置。
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "zj_project.middlewares.ZjProjectSpiderMiddleware": 366,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
USE_PROXY = True

if USE_PROXY:
    DOWNLOADER_MIDDLEWARES = {
        'zj_project.middlewares.ProxyMiddleware': 400,
        #
        "zj_project.middlewares.ZjProjectSpiderMiddleware": 366,
    }
else:
    DOWNLOADER_MIDDLEWARES = { }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}
#上面报的是403，就把403加入。
HTTPERROR_ALLOWED_CODES = [406, ]
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES：项目管道，300为优先级，越低越爬取的优先度越高

if cwd.startswith('/root/crawlab_workspace'):
   # run by scrapy
   ITEM_PIPELINES = {
       'crawlab.scrapy.pipelines.CrawlabPipeline': 300,
       "zj_project.pipelines.SaveAirlineImage": 200,
       'zj_project.pipelines.MongodbPipeline': 400,
   }
else:
    ITEM_PIPELINES = {
        "zj_project.pipelines.SaveAirlineImage": 200,
        'zj_project.pipelines.MongodbPipeline': 400,
    }

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# mongodb配置
if cwd.startswith('/root/crawlab_workspace'):
    MONGO_HOST = "mongo"  # 主机IP
    MONGO_PORT = 27017  # 端口号
else:
    MONGO_HOST = "127.0.0.1"  # 主机IP
    MONGO_PORT = 17017  # 端口号
MONGO_DB = "zjspider"  # 库名
MONGO_USER = "gx" #用户名
MONGO_PSW = "gx301213" #用户密码

# 在setting中设置退出条件
# CLOSESPIDER_TIMEOUT  # 指定时间退出
# CLOSESPIDER_ITEMCOUNT = 500  # 生成了指定数量的item
# CLOSESPIDER_PAGECOUNT = 10  # 抓取了指定数量的响应
# CLOSESPIDER_ERRORCOUNT  # 在发生指定数量的错误

# 打开EXTENSIONS扩展
EXTENSIONS = {
   'scrapy.extensions.closespider.CloseSpider': 500,
}

# ################### ftp配置
# ftp 内的图片目录
IMAGES_STORE_DIR = 'images'
if cwd.startswith('/root/crawlab_workspace'):
    IMAGES_STORE = "ftp://gx:gx301213@localhost:21/images"
    FTP_HOST = "pure-ftpd"
else:
    IMAGES_STORE = "ftp://gx:gx301213@pure-ftpd:21/images"
    FTP_HOST = "localhost"
FTP_USER = 'gx'
FTP_PASS = 'gx301213'
# ################### ftp配置


# filter small image
IMAGES_MIN_HEIGHT = 28
IMAGES_MIN_WIDTH = 28
