# -*- coding: utf-8 -*-
import re
import scrapy


class CboooDetailSpider(scrapy.Spider):
    name = 'cbooo_detail'
    allowed_domains = ['www.cbooo.cn']
    start_urls = ['http://www.cbooo.cn/m/662685']

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

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        week = response.xpath("//td/span/text()").extract()
        week_box_office = response.xpath("//td/span/../text()").extract()
        week_box_office = [re.findall(r"201[0-9]年\s*[0-9]*月[0-9]*日-[0-9]*月[0-9]*日", i) for i in week_box_office]
        week_box_office = [i[0] for i in week_box_office if i]
        cont = response.xpath("//div[@class='cont']/p/text()").extract()
        cont = [i.replace(' ', '').replace('\r', '').replace('\n', '') for i in cont]
        # 片长：130min', '上映时间：2018-9-30（中国）', '制式：2D/IMAX', '国家及地区：中国/中国香港', '发行公司：'
        director = response.xpath("//dl[@class='dltext']/dt[1]/following-sibling::dd[1]/p/a/@title").extract()
        starring = response.xpath("//dl[@class='dltext']/dt[2]/following-sibling::dd[1]/p/a/@title").extract()
        production_company = response.xpath("//dl[@class='dltext']/dt[3]/following-sibling::dd[1]/p/a/@title").extract()
        publish_company = response.xpath("//dl[@class='dltext']/dt[4]/following-sibling::dd[1]/p/a/@title").extract()
        average_per_game = response.xpath("//td[@class='arrow']/text()").extract()
        one_week_box_office = response.xpath("//td[@class='arrow']/following-sibling::td[1]/text()").extract()
        total_box_office = response.xpath("//td[@class='arrow']/following-sibling::td[2]/text()").extract()
        days_released= response.xpath("//td[@class='last']/text()").extract()

        movie_type = cont[3].split("：")[1]
        duration = cont[4].split("：")[1]
        release_time = cont[5].split("：")[1]
        style = cont[6].split("：")[1]

        print({
            "week": week,
            "week_box_office": week_box_office,
            "movie_type": movie_type,
            "duration": duration,
            "release_time": release_time,
            "style": style,
            "publish_company": publish_company,
        })
        print(director)
        print(starring)
        print(production_company)
        print(average_per_game)
        print(one_week_box_office)
        print(total_box_office)
        print(days_released)
        print(len(week_box_office))
