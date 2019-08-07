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
from crawler.items import ArticleItem


class wangyi_news(RedisCrawlSpider):
    name = 'wangyi_news'
    allowed_domains = ['news.sina.com.cn']
    redis_key = 'wangyi_china:start_urls'

    def parse(self, response):

        item = ArticleItem()
        item['website'] = 'news.sina.com.cn'
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@class="main-title"]/text()').extract_first()
        item['content'] = response.xpath('//div[@class="article"]//p/text()').extract()
        item['category'] = response.xpath('//div[@class="channel-path"]//a/text()').extract_first()
        item['publish_time'] = response.xpath('//span[@class="date"]/text()').extract_first()
        yield item



