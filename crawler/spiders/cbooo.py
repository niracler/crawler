# -*- coding: utf-8 -*-
import re

import scrapy
import json
from crawler.items import MovieItem


class CboooSpider(scrapy.Spider):
    name = 'cbooo'
    allowed_domains = ['www.cbooo.cn']
    start_urls = ['http://www.cbooo.cn/movies/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.MoviePipeline': 200,
            # 'crawler.pipelines.CrawlerPipeline': 300,
        },
        'DOWNLOAD_DELAY': 5,
    }

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "bdshare_firstime=1573045320497",
        "Host": "www.cbooo.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
    }

    base_url = "http://www.cbooo.cn/Mdata/getMdata_movie?area={area_id}&type=0&year=2018&initial=%E5%85%A8%E9%83%A8&pIndex={page}"
    area_dict = {}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        """
        获取待爬取的电影列表的列表
        :param response:
        :return:
        """
        area_ids = response.xpath("//select[@id='selArea']/option/@value").extract()
        area = response.xpath("//select[@id='selArea']/option/text()").extract()

        for i, area_id in enumerate(area_ids):
            self.area_dict[area_id] = area[i]
            url = self.base_url.format(area_id=area_id, page=1)
            yield scrapy.Request(url, callback=self.parse_movie, headers=self.headers,
                                 meta={'area_id': area_id, 'page': 1})

    def parse_movie(self, response):
        """
        获取电影基本信息
        :param response:
        :return:
        """
        movie_data = json.loads(response.text)
        page = response.meta.get('page')
        area_id = response.meta.get('area_id')

        # {'pData': [], 'tPage': 0, 'tCount': 0}

        for movie in movie_data['pData']:
            item = MovieItem()
            item['ranking'] = movie['Ranking']
            item['mid'] = movie['ID']
            item['name'] = movie['MovieName']
            item['english_name'] = movie['MovieEnName']
            item['release_year'] = movie['releaseYear']
            item['default_image'] = movie['defaultImage']
            item['box_office'] = movie['BoxOffice']
            item['area'] = self.area_dict[area_id]
            item['area_id'] = area_id

            # yield item

            detail_url = 'http://www.cbooo.cn/m/' + movie['ID']

            yield scrapy.Request(url=detail_url, callback=self.parse_movie_detail, headers=self.headers,
                                 meta={'item': item})

        # 搞定下一页
        if page < movie_data['tPage']:
            next_url = self.base_url.format(area_id=area_id, page=page + 1)
            yield scrapy.Request(url=next_url, callback=self.parse_movie, headers=self.headers,
                                 meta={'area_id': area_id, 'page': page + 1})

    def parse_movie_detail(self, response):
        """
        获取电影详细信息
        :param response:
        :return:
        """

        week = response.xpath("//td/span/text()").extract()
        week_time = response.xpath("//td/span/../text()").extract()
        week_time = [re.findall(r"201[0-9]年\s*[0-9]*月[0-9]*日-[0-9]*月[0-9]*日", i) for i in week_time]
        week_time = [i[0] for i in week_time if i]
        cont = response.xpath("//div[@class='cont']/p/text()").extract()
        cont = [i.replace(' ', '').replace('\r', '').replace('\n', '') for i in cont]

        item = response.meta.get('item')
        item['week'] = week
        item['week_time'] = week_time

        item['director'] = " ".join(response.xpath("//dl[@class='dltext']/dt[1]/following-sibling::dd[1]/p/a/@title").extract())
        item['starring'] = " ".join(response.xpath("//dl[@class='dltext']/dt[2]/following-sibling::dd[1]/p/a/@title").extract())
        item['production_company'] = " ".join(response.xpath(
            "//dl[@class='dltext']/dt[3]/following-sibling::dd[1]/p/a/@title").extract())
        item['publish_company'] = " ".join(response.xpath(
            "//dl[@class='dltext']/dt[4]/following-sibling::dd[1]/p/a/@title").extract())

        item['average_per_game'] = response.xpath("//td[@class='arrow']/text()").extract()
        item['one_week_box_office'] = response.xpath("//td[@class='arrow']/following-sibling::td[1]/text()").extract()
        item['total_box_office'] = response.xpath("//td[@class='arrow']/following-sibling::td[2]/text()").extract()
        item['days_released'] = response.xpath("//td[@class='last']/text()").extract()

        item['movie_type'] = cont[3].split("：")[1]
        item['duration'] = cont[4].split("：")[1]
        item['release_time'] = cont[5].split("：")[1]
        item['style'] = cont[6].split("：")[1]

        yield item
