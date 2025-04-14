import snscrape.modules.twitter as sntwitter
from dotenv import load_dotenv
import os
import requests
from requests.adapters import HTTPAdapter

# 设置代理
proxies = {
    "http": "http://127.0.0.1:50723",
    "https": "http://127.0.0.1:50723",
}

# 创建自定义请求会话并设置代理
session = requests.Session()
session.proxies = proxies
session.mount("http://", HTTPAdapter(max_retries=3))
session.mount("https://", HTTPAdapter(max_retries=3))

# 加载 .env 文件
load_dotenv()
# 获取环境变量（在 .env 文件中存储的 Twitter Cookies）
cookies = {
    'auth_token': os.getenv('SNSCRAPE_TWITTER_COOKIES')
}
session.cookies.update(cookies)

# 将自定义会话传递给 snscrape
sntwitter.TwitterUserScraper.session = session


# 确保 cookies 加载成功
print(f"找到 Twitter Cookies: {cookies}")

# 示例：抓取特定用户的推文
user = "realDonaldTrump"  # 你可以修改为你感兴趣的 Twitter 用户
tweets = []

for tweet in sntwitter.TwitterUserScraper(user).get_items():
    tweets.append({
        "content": tweet.content,
        "date": tweet.date,
        "likes": tweet.likeCount,
        "retweets": tweet.retweetCount
    })

# 输出抓取的推文
for tweet in tweets:
    print(f"{tweet['date']} - {tweet['content']} - Likes: {tweet['likes']} - Retweets: {tweet['retweets']}")