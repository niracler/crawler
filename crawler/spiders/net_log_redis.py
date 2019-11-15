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
        'DOWNLOAD_TIMEOUT': 3,
        'CONCURRENT_REQUESTS': 32,
        # 启用redis
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    }

    def parse(self, response):
        net_log = NetLogItem()
        net_log['url'] = response.url
        net_log['urldata'] = response.text
        net_log['update'] = str(datetime.now())
        yield net_log
