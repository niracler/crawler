import time
import redis
import codecs
import csv
import os
import random
import re
import requests
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from lxml import etree
from time import sleep
from tqdm import tqdm

client = redis.Redis(host='10.42.30.245', port='6379', password='123456')
cookie = {
    "Cookie": "SCF=Al7vbWHPPiGpmRGfvae44UBnUnmbohaqka8ZGIUsNE07HaGElIstfhNv5LLtRskQ0lVgicH7WqEF1EFDBcLHebU.; _T_WM=73238227473; MLOGIN=1; SUB=_2A25x67c9DeRhGeBK6lcX-CrJyDiIHXVTF9l1rDV6PUJbkdBeLRnckW1NR_3Syh9jf0I8NkVbbdbpoNFBfEKGwZdG; SUHB=0rr7CHUMwD09f5; SSOLoginState=1559218029; M_WEIBOCN_PARAMS=luicode%3D20000174",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}  # 将your cookie替换成自己的cookie
url = "https://weibo.cn/1736472255/follow"
html = requests.get(url, cookies=cookie).content
selector = etree.HTML(html)

page_num = 1
try:
    if selector.xpath("//input[@name='mp']") == []:
        page_num = 1
    else:
        page_num = (int)(selector.xpath("//input[@name='mp']")[0].attrib["value"])
except Exception as e:
    print("Error: ", e)
    traceback.print_exc()

res = []
page1 = 0
random_pages = random.randint(1, 5)
for page in range(1, page_num + 1):
    url = "https://weibo.cn/1736472255/follow?page={}"
    html = requests.get(url.format(page), cookies=cookie).content
    selector = etree.HTML(html)
    s = selector.xpath("//td/a[2]")
    for i in range(len(s)):
        s1 = s[i].attrib["href"]
        user_id = re.search(r'.*?uid=(\d+)', s1).groups()[0]
        url = "https://weibo.cn/u/{}".format(user_id)
        res.append(url)
        client.lpush("weibo_user_redis:start_urls", url)
    print(page)

    # 通过加入随机等待避免被限制。爬虫速度过快容易被系统限制(一段时间后限
    # 制会自动解除)，加入随机等待模拟人的操作，可降低被系统限制的风险。默
    # 认是每爬取1到5页随机等待6到10秒，如果仍然被限，可适当增加sleep时间
    if page - page1 == random_pages:
        sleep(random.randint(6, 10))
        page1 = page
        random_pages = random.randint(1, 5)

