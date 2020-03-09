# -*- coding: utf-8 -*-
import re

import scrapy
from crawler.items import ArticleItem
from scrapy_redis.spiders import RedisCrawlSpider, RedisSpider
from zhconv import convert

class GnnSpider(RedisCrawlSpider):
    name = 'gnn_redis'
    redis_key = 'gnn_redis:start_urls'
    item_index = 'url'
    custom_settings = {
        'ITEM_PIPELINES' : {
            'crawler.pipelines.ArticlePipeline':300
            # 'crawler.pipelines.CrawlerPipeline': 300,
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
            # 'crawler.pipelines.MongoPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.ProxyMiddleware': 1,
        },
        # 启用redis
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    }

    def parse(self, response):
        articles = response.xpath("//div[@class='GN-lbox2B']")
        for article in articles:
            url = article.xpath('h1/a/@href').extract_first()
            if url:
                url = 'https:' + url
                item = ArticleItem()
                item['website'] = 'https://gnn.gamer.com.tw'
                title = article.xpath("h1/a/text()").extract_first()
                item['title'] = convert(title, 'zh-cn')
                yield scrapy.Request(url=url, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta.get('item')
        item['url'] = response.url
        content = " ".join(response.xpath('string(//div[@class="GN-lbox3B"]/div)').extract())
        item['content'] = self.parse_content(content)
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
        content = " ".join(response.xpath('string(//div[@class="MSG-list8C"])').extract())
        item['content'] = self.parse_content(content)
        item['category'] = "无"
        try:
            item['publish_time'] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", response.text).group(0)
        except Exception as e:
            item['publish_time'] = "1018-12-22 14:36:00"

        yield item

    def parse_content(self, content):
        content = content.replace(r'【.*?】', '')
        content = content.replace('\u3000', '')
        content = content.replace('\n', '')
        content = content.replace('\r', '')
        content = content.replace('\xa0', '')
        content = content.replace('-', '')
        content = content.replace('17173新闻采访部', '')
        content = content.replace(r'/[a-zA-Z]*[:\//\]*[A-Za-z0-9\-_]+\.+[A-Za-z0-9\.\/%&=\?\-_]+/i', '')
        content = content.strip()
        content = convert(content, 'zh-cn')  # 将内容进行简繁体字转换

        return content
