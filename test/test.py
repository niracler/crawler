import requests
import re
from lxml import etree
import redis
client = redis.Redis(host='centos-l1-vm-01.niracler.com', port='6379', password='123456')
base_url = 'https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page={}&encode=utf-8&callback=feedCardJsonpCallback'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

urls = []

for i in range(5, 50):
    res = requests.get(base_url.format(i), headers=headers)
    urls.extend(re.findall('"url":"(.*?)"', res.text))

urls = list(map(lambda x: x.replace('\\', ''), urls))

for url in urls:
    client.lpush("wangyi_china:start_urls", url)

print(urls)