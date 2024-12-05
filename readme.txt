# 命令记录
scrapy startproject 项目名

scrapy genspider 爬虫名 域名

scrapy crawl 爬虫名

# 下面演示创建项目的例子

scrapy startproject zj_project

cd zj_project

scrapy genspider baidu www.baidu.com
scrapy genspider baiduhangzhan www.baidu.com

# 新曾飞机爬虫
scrapy genspider airlines www.airliners.net
## 开始爬取
scrapy crawl airlines

# 新曾环球医疗器械网
https://ylqx.qgyyzs.net/zs/list_8_1_0_1.htm
https://ylqx.qgyyzs.net/zs/list_0_0_0_2753.htm

scrapy genspider ylqx ylqx.qgyyzs.net
scrapy crawl ylqx
### 保存日志
crawl ylqx --logfile ylqx_log.log

# xpath 使用方法
https://blog.csdn.net/heartbeat196/article/details/113790232

# 下载医疗数据集
./hfd.sh  FreedomIntelligence/huatuo_encyclopedia_qa --hf_username perfectbullet --hf_token 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

# 反爬设置
#开启访问频率限制
AUTOTHROTTLE_ENABLED = True
#设置访问开始的延迟
AUTOTHROTTLE_START_DELAY = 5
#设置访问之间的最大延迟
AUTOTHROTTLE_MAX_DELAY = 60
#设置Scrapy 并行发给每台远程服务器的请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#设置下裁之后的自动延迟
DOWNLOAD_DELAY = 3

# 项目git
git@github.com:perfectbullet/zj_spider.git

# 项目启动
(base) ubuntu@ubuntu-desktop-2204:/data/spider_new/zj_spider$ python3.10 -m venv venv
(base) ubuntu@ubuntu-desktop-2204:/data/spider_new/zj_spider$ source venv/bin/activate
(venv) (base) ubuntu@ubuntu-desktop-2204:/data/spider_new/zj_spider$ conda deactivate
(venv) ubuntu@ubuntu-desktop-2204:/data/spider_new/zj_spider$
