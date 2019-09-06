# -*- coding: utf-8 -*-
import scrapy
from crawler.items import ThreeDMOLGame
import requests
from crawler.tool import random_filename

class ThreeDMOLGameSpider(scrapy.Spider):
    name = 'games_3dm_ol_spider'
    item_index = 'name'
    allowed_domains = ['ol.3dmgame.com']
    start_urls = ['https://ol.3dmgame.com/ku/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    custom_settings = {
        'MONGODB_COLLECTION': 'games_3dm_ol',
        'ITEM_PIPELINES': {
            # 'crawler.pipelines.CrawlerPipeline': 300,
            'crawler.pipelines.ImgDownloadPipeline': 300,
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
            'crawler.pipelines.MongoPipeline': 400,
        }
    }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = ThreeDMOLGame()
        lists = response.xpath('//ul[@class="ul1"]/li')
        for i in lists:
            item = self.deal_with_data(item=item, response=i)
            if item:
                yield item

        next = response.xpath('//div[@class="fenye"]/ul/li[@class="next"]/a/@href').extract_first()
        if next:
            yield scrapy.Request(next, headers=self.headers, callback=self.parse)

    def deal_with_data(self, item, response):
        # 将数据规范化
        try:
            item['name'] = response.xpath('div[2]/div[1]/div/a/text()').extract_first()
            item['publish_time'] = response.xpath('div[2]/div[3]/p[2]/i/text()').extract_first()
            item['popularity'] = response.xpath('div[2]/div[2]/p[1]/i/text()').extract_first()
            item['developer'] = response.xpath('div[2]/div[3]/p[1]/i/text()').extract_first()
            item['state'] = response.xpath('div[2]/div[1]/p[2]/i/text()').extract_first()
            item['category'] = '网游 ' + response.xpath('div[2]/div[1]/p[1]/i/a/text()').extract_first()
            item['publisher'] = response.xpath('div[2]/div[2]/p[3]/i/text()').extract_first()
            item['popularity'] = response.xpath('div[2]/div[2]/p[2]/i/a/text()').extract_first()
            item['score'] = response.xpath('div[2]/div[3]/div[2]/font/text()').extract_first()
            img_url = response.xpath('div[1]/a/img/@src').extract_first()
            filename = random_filename(img_url)
            item['img_url'] = img_url
            item['img_path'] = '/media/' + filename
            # with open('/home/zzh/图片/Threedmgame/'+filename, 'wb') as f:
            #     f.write(requests.get(url=img_url, headers=self.headers).content)
            return item
        except Exception as e:
            print(e)
            return None
