# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItem(scrapy.Item):
    website = scrapy.Field()  # 所爬取的网站的名称
    url = scrapy.Field()  # 文章链接
    title = scrapy.Field()  # 文章标题
    content = scrapy.Field()  # 文章内容
    category = scrapy.Field()  # 文章类型
    publish_time = scrapy.Field()  # 发布时间


class ShensheArticleItem(scrapy.Item):
    article_url = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    magnet = scrapy.Field()
    datetime = scrapy.Field()
    comments = scrapy.Field()
    comment_source = scrapy.Field()
    score = scrapy.Field()
    score_nums = scrapy.Field()
    img_url = scrapy.Field()
