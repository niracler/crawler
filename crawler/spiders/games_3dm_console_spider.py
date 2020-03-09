# -*- coding: utf-8 -*-
import scrapy
from crawler.items import ThreeDMConsoleGame, ThreeDMOLGame, ThreeDMShouYouGame
import requests
from crawler.tool import random_filename
import re


class Games3dmSpider(scrapy.Spider):
    name = 'games_3dm_console_spider'
    item_index = 'name'
    allowed_domains = ['www.3dmgame.com']
    start_urls = ['https://www.3dmgame.com/games/zq_1/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.ImgDownloadPipeline': 300,
            'crawler.pipelines.GamePipeline':300
        },
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = ThreeDMConsoleGame()
        lists = response.xpath('//div[@class="ztliswrap"]/div[@class="lis"]')
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
            item['name'] = '-'.join(
                [response.xpath('a[@class="bt"]/text()').extract_first().strip(),
                 response.xpath('a[@class="bt"]/span/text()').extract_first()])
            item['publish_time'] = response.xpath('ul[@class="info"]/li[1]/text()').extract_first().split('：')[-1]
            mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",item['publish_time'])
            if mat:
                item['publish_time'] = mat.group(0)
            else :
                item['publish_time'] = ""

            item['publisher'] = response.xpath('ul[@class="info"]/li[2]/text()').extract_first().split('：')[-1]
            item['developer'] = response.xpath('ul[@class="info"]/li[3]/text()').extract_first().split('：')[-1]
            item['platform'] = response.xpath('ul[@class="info"]/li[4]/text()').extract_first().split('：')[-1]
            item['category'] = '单机 ' + response.xpath('ul[@class="info"]/li[5]/text()').extract_first().split('：')[-1]
            item['language'] = response.xpath('ul[@class="info"]/li[6]/text()').extract_first().split('：')[-1]
            item['description'] = response.xpath('div[@class="miaoshu"]/text()').extract_first().replace('\n', '').strip()
            item['score'] = response.xpath('div[@class="pfbox"]//font/text()').extract_first()
            img_url = response.xpath('a[@class="img"]/img/@src').extract_first()
            filename = random_filename(img_url)
            item['img_url'] = img_url
            item['img_path'] = '/images/' + filename

            return item
        except Exception as e:
            print(e)
            return None


