import redis
import random
import requests
from lxml import etree
from time import sleep

client = redis.Redis(host='10.42.41.214', port='6379', password='123456')
cookie = {
    "Cookie": "ALF=1562988467; SCF=Ar8pWoKQ1zoyUpUdFA28Qhsn20_bd1JIrQcizqZWdmYYD_5ItY272bxOa4sQ85odTHzYuWvWZtg63ogObA_xAZs.; SUB=_2A25wBbLkDeRhGeNM6lUS9SfJyDqIHXVTCd6srDV6PUNbktANLUf8kW1NTijfmh7bWTR2kM_3cUrdjnjfZVq-5Tr1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW7MEMZijfvn_S.1HAKvq155JpX5KMhUgL.Fo-EeKM0SK.fe0q2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfeo2Ne0-4SKec; SUHB=0ebdRvnTsT2xjK; SSOLoginState=1560396468; _T_WM=cfadc69e7e6a3ff87862a2e789f04448",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}  # 将your cookie替换成自己的cookie

while True:
    url = client.lpop('weibo_info_redis:start_urls')
    if not url:
        print("结束")
        break
    html = requests.get(url, cookies=cookie).content
    selector = etree.HTML(html)

    base_info = selector.xpath('/html/body/div[7]/text()')
    other_info = selector.xpath('/html/body/div[9]/text()')

    user_info = {
        'id': str(url).split('/')[-2],
        'base_info': base_info,
        'other_info': other_info
    }
    user_info = str(user_info)
    print(user_info)

    client.lpush("weibo_info_redis:items", user_info)

    sleep(random.randint(6, 10))
