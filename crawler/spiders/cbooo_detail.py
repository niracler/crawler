# -*- coding: utf-8 -*-
import scrapy


class CboooDetailSpider(scrapy.Spider):
    name = 'cbooo_detail'
    allowed_domains = ['www.cbooo.cn']
    start_urls = ['http://www.cbooo.cn/m/678141']

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
        title = response.xpath("//td[@class='bgtop']//text()").extract()
        week = response.xpath("//td/span/text()").extract()
        bgtop = response.xpath("//td[@class='bgtop']//text()").extract()
        # detail = [ if i for i in detail]

        print({
            "week": week,
            "bgtop": bgtop,
        })
