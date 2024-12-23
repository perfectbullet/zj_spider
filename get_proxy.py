import requests
import re

url = "https://ylqx.qgyyzs.net/business/zs267860.htm"

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
    with open('./proxy_pages/proxy_pagesv1.txt', mode='rt', encoding='utf8') as f:
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
                    resp = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                    if resp.status_code == 200:
                        print(ip_port)
                except Exception as e:
                    pass
