# -*- coding: utf-8 -*-
import scrapy
from crawler.items import ThreeDMShouYouGame
import requests
from crawler.tool import random_filename

class ThreedmconsolegameSpider(scrapy.Spider):
    name = 'games_3dm_shouyou_spider'
    allowed_domains = ['shouyou.3dmgame.com']
    start_urls = ['https://shouyou.3dmgame.com/zt/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    base_url = 'https://shouyou.3dmgame.com'
    custom_settings = {
        'MONGODB_COLLECTION': 'entity',
        'ITEM_PIPELINES': {
            'crawler.pipelines.ImgDownloadPipeline': 300,
            'crawler.pipelines.MongoPipeline': 400,
        },
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'SCHEDULER': 'scrapy.core.scheduler.Scheduler'
    }
    item_index = 'name'
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = ThreeDMShouYouGame()
        lists = response.xpath('//div[@class="warp_post"]/ul/li')
        for i in lists:
            item = self.deal_with_data(item=item, response=i)
            if item:
                yield item

        next = response.xpath('//div[@class="pagewrap"]/ul/li[@class="next"]/a/@href').extract_first()
        if next:
            yield scrapy.Request(next, headers=self.headers, callback=self.parse)

    def deal_with_data(self, item, response):
        # 将数据规范化
        try:
            item['name'] = response.xpath('div[2]/a/text()').extract_first()
            item['category'] = response.xpath('div[2]/p[1]/span[1]/text()').extract_first().split('：')[-1]
            item['language'] = response.xpath('div[2]/p[1]/span[2]/text()').extract_first().split('：')[-1]
            item['volume'] = response.xpath('div[2]/p[1]/span[3]/text()').extract_first().split('：')[-1]
            # 判断 a1 为安卓， a2 为苹果
            platform = response.xpath('div[2]/p[2]/span[1]/a/@class').extract()
            if 'a1' in platform and 'a2' in platform:
                item['platform'] = '安卓 苹果'
            elif 'a1' in platform:
                item['platform'] = '安卓'
            elif 'a2' in platform:
                item['platform'] = '苹果'
            else:
                item['platform'] = '未知'
            publisher = response.xpath('div[2]/p[2]/span[2]/text()').extract_first().split('：')[-1]
            if not publisher:
                publisher = '未知'
            item['publisher'] = '手游 ' + publisher
            item['publish_time'] = response.xpath('div[2]/p[2]/span[3]/text()').extract_first().split('：')[-1]
            item['description'] = response.xpath('div[2]/p[3]/text()').extract_first().replace('\n', '').strip()
            item['score'] = response.xpath('div[2]/div/div[2]/text()').extract_first()
            img_url = self.base_url + response.xpath('div[1]/a/img/@src').extract_first()
            filename = random_filename(img_url)
            item['img_url'] = img_url
            item['img_path'] = '/media/' + filename
            return item
        except Exception as e:
            print(e)
            return None
