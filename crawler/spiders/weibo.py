# -*- coding: utf-8 -*-
import traceback
import scrapy
from crawler.spiders.weiboSpider import WeiboSpider
from crawler.items import WeiboUserItem

class Weibo(scrapy.Spider):
    name = 'weibo2'
    allowed_domains = ['www.liuli.in']
    start_urls = ['https://www.liuli.in/wp']

    # 1736472255

    def parse(self, response):
        try:
            # 使用实例,输入一个用户id，所有信息都会存储在wb实例中
            user_id = 1669879400  # 可以改成任意合法的用户id（爬虫的微博id除外）
            filter = 1  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
            wb = WeiboSpider(user_id, filter)  # 调用Weibo类，创建微博实例wb
            wb.start()  # 爬取微博信息
            item = WeiboUserItem()
            item['user_id'] = wb.user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
            item['nickname'] = wb.nickname  # 用户昵称，如“Dear-迪丽热巴”
            item['weibo_num'] = wb.weibo_num  # 用户全部微博数
            item['got_num'] = wb.got_num  # 爬取到的微博数
            item['following'] = wb.following  # 用户关注数
            item['followers'] = wb.followers # 用户粉丝数
            item['weibo'] = wb.weibo
            yield item
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()



    # articles = response.css('#content article')
    # for article in articles:
    #     url = article.css('header h1 a::attr(href)').extract_first()
    #     if url:
    #         item = ShensheArticleItem()
    #         item['article_url'] = url
    #         item['img_url'] = article.css('.entry-content img::attr(src)').extract_first()
    #         yield scrapy.Request(url=url, callback=self.parse_item, meta={'item': item})
    #
    # next_url = response.xpath('//div[@id="wp_page_numbers"]/ul/li[last()]/a/@href').extract_first()
    #
    # if next_url:
    #     yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_item(self, response):
        pass
        # item = response.meta.get('item')
        # item['title'] = response.css('#content article header > h1::text').extract_first()
        # item['author'] = response.css('#content article header > div .by-author a::text').extract_first()
        # item['datetime'] = response.css('#content article header > div > a > time::text').extract_first()
        # # item['content'] = response.css('#content article .entry-content::text').extract_first()
        # item['magnet'] = 'magnet:?xt=urn:btih:' + response.xpath(
        #     '//div[@id="content"]//div[@class="entry-content"]//text()').re_first('[0-9|a-z|A-Z]{40}')
        # item['comment_source'] = response.css('#comments-title span::text').extract_first()
        # item['comments'] = response.xpath('//h2[@id="comments-title"]/text()').re_first('(\d+)')
        # item['score'] = response.xpath('//div[@id="content"]/article/div[@class="entry-header"]'
        #                                '/div[@class="post-ratings"]/strong[2]/text()').extract_first()
        # item['score_nums'] = response.xpath('//div[@id="content"]/article/div[@class="entry-header"]'
        #                                     '/div[@class="post-ratings"]/strong[1]/text()').extract_first()
        # yield item
