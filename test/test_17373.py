import requests
import re
from lxml import etree
import redis
import time
client = redis.Redis(host='centos-l1-vm-01.niracler.com', port='6379', password='123456')
base_url = 'http://search.17173.com/web/search.do?index-name=WEBPAGE&keyword=&page-no={' \
           '}&page-size=15&expression=newsChannel%3A10009+AND+(newsKind%3A{' \
           '})+AND+newsClass%3A1&highLights=newsTitle%2CnewsContent&sort-reverse=true&sort-type=STRING&sort-by' \
           '=newsDate '

# china_id = '10019'
# world_id = '10152'
# korea_id = '27060'
# product_id = '10161'
# news_id = '10149'
category_ids = ['10019', '10152', '27060', '10161', '10149']

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Host': 'search.17173.com',
    'Upgrade-Insecure-Requests': '1'
}

urls = []
count = 0
validate = ''

pattern = re.compile('"newsUrl":"(.*?)"')

for id in category_ids:
    i = 1
    print('正在存储id为 %s 的站点 ====================>>>' % id)
    while True:
        try:
            res = requests.get(base_url.format(i, id), headers=headers)
            # urls = re.findall('"newsUrl":"(.*?)"', res.text)
            urls = pattern.findall(res.text)

            if urls:
                if validate == urls[0]:
                    break
                else:
                    validate = urls[0]
                for url in urls:
                    print('正在将url: %s 写入数据库' % url)
                    client.lpush("17373_game:start_urls", url)
                    count += 1
                print('===============================================================================================')
                i += 1
            else:
                break
        except:
            print('请求过于频繁，沉睡5秒')
            print('ZZzzzzz~')
            time.sleep(5)

print('一共存储了 %d 条url' % count)

print(urls)