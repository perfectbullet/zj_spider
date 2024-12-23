import requests
import re

url = "https://3618med.com/product/p1.html"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
headers = {
       'User-Agent':USER_AGENT
}

if __name__ == '__main__':
    # 测试代理ip
    # open https://cn.proxy-tools.com/proxy/https?page=1
    # copy the page content then copy into  proxy_pages/proxy_pagesv1.txt
    # ran this scripts
    # 是否可用， 并打印可用的ip和端口
    ip_port = []
    with open('./proxy_pages/proxy_pagesv1.txt', mode='rt', encoding='utf8') as f, open('./proxy_list.txt', mode='w', encoding='utf8') as f2:
        for line in f:
            mt = re.match(r'(\d+\.\d+\.\d+\.\d+)\t(\d+)\t\w+\t.*\t.*\n', line)
            if mt is not None:
                ip_port = '{}:{}'.format(mt.group(1), mt.group(2))
                proxy = 'http://' + ip_port
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
                try:
                    # 可以使用aiohttp 获得更高的并法
                    resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                    if resp.status_code == 200:
                        f2.write(ip_port + '\n')
                except Exception as e:
                    pass
