# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from crawler.items import ArticleItem


class Game17373Spider(RedisCrawlSpider):
    name = 'game_17373'
    allowed_domains = ['news.17173.com']
    redis_key = '17373_game:start_urls'

    custom_settings = {
        'ITEM_PIPELINES' : {
            'crawler.pipelines.ArticlePipeline':300
        },
        # 启用redis
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    }

    def parse(self, response):
        item = ArticleItem()
        item['website'] = 'news.17173.com'
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@class="gb-final-tit-article"]/text()').extract_first()
        item['content'] = self.parse_content('-'.join(response.xpath('//div[@id="mod_article"]//text()').extract()))
        item['category'] = '游戏'
        item['publish_time'] = response.xpath('//div[@class="gb-final-mod-info"]/span[1]/text()').extract_first()
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

        return content