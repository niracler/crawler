# -*- coding: utf-8 -*-
import re

import scrapy
from crawler.items import ArticleItem
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider


class GnnSpider(RedisCrawlSpider):
    name = 'gnn_redis'
    redis_key = 'gnn_redis:start_urls'
    item_index = 'url'
    custom_settings = {
        'MONGODB_COLLECTION': 'gnn_game',
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.ProxyMiddleware': 1,
        }
    }

    def parse(self, response):
        articles = response.xpath("//div[@class='GN-lbox2B']")
        for article in articles:
            url = article.xpath('h1/a/@href').extract_first()
            if url:
                url = 'https:' + url
                item = ArticleItem()
                item['website'] = 'https://gnn.gamer.com.tw'
                item['title'] = article.xpath("h1/a/text()").extract_first()
                yield scrapy.Request(url=url, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta.get('item')
        item['url'] = response.url
        item['content'] = " ".join(response.xpath('string(//div[@class="GN-lbox3B"]/div)').extract())
        item['category'] = " ".join(response.xpath('//ul[@class="platform-tag"]/li/a/text()').extract())

        try:
            item['publish_time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", response.text).group(0)
        except Exception as e:
            item['publish_time'] = "1018-12-22 14:36:00"

        # 假如是那种js重定向的页面
        if item['content'] == '':
            url = re.findall(r"replace\('(.*?)'\)", response.text)[0]
            yield scrapy.Request(url=url, callback=self.parse_item2, meta={'item': item})
        else:
            yield item

    def parse_item2(self, response):
        item = response.meta.get('item')
        item['url'] = response.url
        item['content'] = " ".join(response.xpath('string(//div[@class="MSG-list8C"])').extract())
        item['category'] = "无"
        try:
            item['publish_time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", response.text).group(0)
        except Exception as e:
            item['publish_time'] = "1018-12-22 14:36:00"

        yield item
