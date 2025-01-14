import requests

proxies = {
                    'http': 'http://192.168.250.1:7897',
                    'https': 'http://192.168.250.1:7897',
                }

response = requests.get('https://zh.wikipedia.org/wiki/%E8%A9%B9%E5%A7%86%E6%96%AF%C2%B7%E8%8C%83%C2%B7%E8%89%BE%E5%80%AB', proxies=proxies)