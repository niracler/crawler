# -*- coding: utf-8 -*-
import scrapy
from crawler.items import GameSky
import requests
from crawler.tool import random_filename

class GameSkySpider(scrapy.Spider):
    name = 'gamesky'
    allowed_domains = ['ku.gamersky.com']
    start_urls = ['http://ku.gamersky.com/release/pc_201908/']
    base_url = 'ku.gamersky.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    custom_settings = {
        'MONGODB_COLLECTION': 'entity',
        'ITEM_PIPELINES': {
            #'crawler.pipelines.CrawlerPipeline': 300,
            'crawler.pipelines.ImgDownloadPipeline': 300,
            # 'scrapy_redis.pipelines.RedisPipeline': 400,
            'crawler.pipelines.MongoPipeline': 400,
        }
    }
    item_index = 'name'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//div[@class="nav"]/a/@href').extract() # 提取分类页面
        for relate_url in urls:
            yield scrapy.Request(url=response.urljoin(relate_url), headers=self.headers, callback=self.parse_page)

    def parse_page(self, response):
        list_urls = response.xpath('//ul[@class="SH"]/li[@class="list none"]')  # 右侧列表链接
        for per_year in list_urls:
            divs = per_year.xpath('div')
            for per_month in divs:
                url = response.urljoin(per_month.xpath('a/@href').extract_first())
                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_item)

    def parse_item(self, response):
        item = GameSky()
        lists = response.xpath('//ul[@class="PF"]/li')
        if lists:
            # 判断右侧当月是否有游戏发行
            for i in lists:
                item = self.deal_with_data(item=item, response=i)
                yield item

    def deal_with_data(self, item, response):
        # 将数据规范化
        category = response.xpath('//div[@class="nav"]/a[contains(@class, "cur")]/text()').extract_first()  # 获取大分类
        item['name'] = response.xpath('div[1]/div[2]/a/text()').extract_first()
        item['publish_time'] = response.xpath('div[1]/div[3]/text()').extract_first().split('：')[-1].strip()
        item['category'] = ' '.join([category, response.xpath('div[1]/div[4]/a/text()').extract_first()])
        item['publisher'] = response.xpath('div[1]/div[5]/text()').extract_first().split('：')[-1].strip()
        item['description'] = response.xpath('div[1]/div[6]/p/text()').extract_first().replace('\r\n', '').replace('\u3000', '').strip()
        img_url = response.xpath('div[1]/div[1]//img/@src').extract_first()
        filename = random_filename(img_url)
        item['img_url'] = img_url
        item['img_path'] = '/media/' + filename
        # with open('/home/zzh/图片/Threedmgame/'+filename, 'wb') as f:
        #     f.write(requests.get(url=img_url, headers=self.headers).content)
        return item
