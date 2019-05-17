# -*- coding: utf-8 -*-
import scrapy
from crawler.items import ShensheArticleItem
from scrapy_redis.spiders import RedisCrawlSpider


class ShensheSpider(RedisCrawlSpider):
    name = 'shenshe_redis'
    allowed_domains = ['www.liuli.in']
    redis_key = 'shenshe:start_urls'

    def parse(self, response):
        articles = response.css('#content article')
        for article in articles:
            url = article.css('header h1 a::attr(href)').extract_first()
            if url:
                item = ShensheArticleItem()
                item['article_url'] = url
                item['img_url'] = article.css('.entry-content img::attr(src)').extract_first()
                yield scrapy.Request(url=url, callback=self.parse_item, meta={'item': item})

    def parse_item(self, response):
        item = response.meta.get('item')
        item['title'] = response.css('#content article header > h1::text').extract_first()
        item['author'] = response.css('#content article header > div .by-author a::text').extract_first()
        item['datetime'] = response.css('#content article header > div > a > time::text').extract_first()
        item['magnet'] = 'magnet:?xt=urn:btih:' + response.xpath(
            '//div[@id="content"]//div[@class="entry-content"]//text()').re_first('[0-9|a-z|A-Z]{40}')
        item['comment_source'] = response.css('#comments-title span::text').extract_first()
        item['comments'] = response.xpath('//h2[@id="comments-title"]/text()').re_first('(\d+)')
        item['score'] = response.xpath('//div[@id="content"]/article/div[@class="entry-header"]'
                                       '/div[@class="post-ratings"]/strong[2]/text()').extract_first()
        item['score_nums'] = response.xpath('//div[@id="content"]/article/div[@class="entry-header"]'
                                            '/div[@class="post-ratings"]/strong[1]/text()').extract_first()
        yield item
