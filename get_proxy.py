####
import requests
url = "https://ylqx.qgyyzs.net/business/zs267860.htm"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
headers = {
       'User-Agent':USER_AGENT
}

with open('./proxy_listv2.txt', mode='rt', encoding='utf8') as f:
    for line in f:
        ip_port = line.strip()
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
