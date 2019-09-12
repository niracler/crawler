from crawler.items import NetLogItem
from scrapy_redis.spiders import RedisCrawlSpider
from datetime import datetime


class NetLogSpider(RedisCrawlSpider):
    name = 'net_log'
    redis_key = 'net_log:start_urls'
    item_index = 'url'
    custom_settings = {
        'MONGODB_COLLECTION': 'net_log',
        'DOWNLOAD_DELAY': 0,
        'DOWNLOAD_TIMEOUT': 5,
    }

    def parse(self, response):
        net_log = NetLogItem()
        net_log['url'] = response.url
        net_log['urldata'] = " ".join(response.xpath('//text()').extract())
        net_log['update'] = str(datetime.now())
        yield net_log
