# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisCrawlSpider
from crawler.items import ArticleItem


class Game17373Spider(RedisCrawlSpider):
    name = 'game_17373'
    allowed_domains = ['news.17173.com']
    redis_key = '17373_game:start_urls'

    custom_settings = {
        'MONGODB_COLLECTION': '17373_game',
    }

    def parse(self, response):
        item = ArticleItem()
        item['website'] = 'news.17173.com'
        item['url'] = response.url
        item['title'] = response.xpath('//h1[@class="gb-final-tit-article"]/text()').extract_first()
        item['content'] = '-'.join(response.xpath('//div[@id="mod_article"]//text()').extract())
        item['category'] = '游戏'
        item['publish_time'] = response.xpath('//div[@class="gb-final-mod-info"]/span[1]/text()').extract_first()
        yield item