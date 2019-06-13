# -*- coding: utf-8 -*-

from random import random
import redis
import json
import random
import traceback
from time import sleep
import requests
import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisCrawlSpider
from crawler.items import WeiboUserItem


class WeiboUser(RedisCrawlSpider):
    name = 'weibo_user_redis'
    allowed_domains = ['weibo.cn']
    redis_key = 'weibo_user_redis:start_urls'

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

        items = self.cookie_json['Cookie2'].split(';')
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
        user_item = WeiboUserItem()
        user_id = int(response.url.split('/')[-1])
        user_item['user_id'] = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        user_item['nickname'] = response.xpath("//title/text()").extract_first()[0:-3]  # 用户昵称，如“Dear-迪丽热巴”

        user_info = response.xpath("//div[@class='tip2']/*/text()").extract()

        user_item['weibo_num'] = int(user_info[0][3:-1])  # 用户全部微博数
        user_item['following'] = int(user_info[1][3:-1])  # 用户关注数
        user_item['followers'] = int(user_info[2][3:-1])  # 用户粉丝数

        # 将content的url放进redis
        page_num = self.get_page_num(response)
        for page in range(1, page_num + 1):
            url = "https://weibo.cn/u/{0}?page={1}".format(user_id, page)
            self.client.lpush("weibo_content_redis:start_urls", url)

        # 将follow的url放进redis
        url = "https://weibo.cn/{0}/follow".format(user_id)
        html = requests.get(url, cookies=self.cookie).content
        selector = etree.HTML(html)
        page_num = self.get_page_num(selector)

        for page in range(1, page_num + 1):
            url = "https://weibo.cn/{0}/follow?page={1}".format(user_id, page)
            self.client.lpush("weibo_follow_redis:start_urls", url)

        sleep(random.randint(6, 10))

        yield user_item

    # def parse_(self, response):


    def get_page_num(self, response):
        """获取微博总页数"""
        try:
            if response.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(
                    response.xpath("//input[@name='mp']")[0].attrib["value"])
            return page_num
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

