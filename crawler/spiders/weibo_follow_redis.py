# -*- coding: utf-8 -*-

from random import random
import redis
import json
import random
import re
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from time import sleep
import requests
import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisCrawlSpider
from tqdm import tqdm
from crawler.items import WeiboUserItem, WeiboFollowItem


class WeiboFollow(RedisCrawlSpider):
    name = 'weibo_follow_redis'
    allowed_domains = ['weibo.cn']
    redis_key = 'weibo_follow_redis:start_urls'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = redis.Redis(host='10.42.31.236', port='6379', password='123456')  # 连接redis
        self.filter = 1
        self.got_num = 0  # 爬取到的微博数
        self.weibo = []
        itemDict = {}

        try:
            with open('cookie.json') as f:
                self.cookie_json = json.loads(f.read())
        except:
            self.cookie = {}

        items = self.cookie_json['Cookie'].split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        self.cookie = itemDict

        print(self.cookie)

    def make_requests_from_url(self, url):
        self.headers = {
            'Connection': 'keep - alive',
            'User-Agent': self.cookie_json["user-agent"]
        }
        return scrapy.Request(url=url, headers=self.headers, cookies=self.cookie, callback=self.parse)

    def parse(self, response):

        s = response.xpath("//td/a[2]")
        for i in range(len(s)):
            # 拿出关注用户的id
            s1 = s[i].attrib["href"]
            follow_id = re.search(r'.*?uid=(\d+)', s1).groups()[0]

            # 构造关注用户的url
            url = "https://weibo.cn/u/{}".format(follow_id)
            self.client.lpush("weibo_user_redis:start_urls", url)

            # 将关系存进数据库
            follow_item = WeiboFollowItem()
            user_id = int(response.url.split('/')[-2])
            follow_item['user_id'] = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
            follow_item['follow_id'] = follow_id
            yield follow_item

        sleep(random.randint(6, 10))


