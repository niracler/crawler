# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    ranking = scrapy.Field()  # 排名
    mid = scrapy.Field()  # ID
    name = scrapy.Field()  # 电影名
    english_name = scrapy.Field()  # 英文名
    release_year = scrapy.Field()  # 上映年限
    default_image = scrapy.Field()  # 图片
    box_office = scrapy.Field()  # 票房
    area = scrapy.Field()  # 地区
    area_id = scrapy.Field()  # 地区ID
    week = scrapy.Field()  # 周数
    week_time = scrapy.Field()  # 每周时间
    average_per_game = scrapy.Field()  # 平均每场人次
    one_week_box_office = scrapy.Field()  # 周票房
    total_box_office = scrapy.Field()  # 总票房
    days_released = scrapy.Field()  # 上映天数
    director = scrapy.Field()  # 导演
    starring = scrapy.Field()  # 明星
    production_company = scrapy.Field()  # 制作公司
    publish_company = scrapy.Field()  # 出版公司
    movie_type = scrapy.Field()  # 电影类型
    duration = scrapy.Field()  # 片长
    release_time = scrapy.Field()  # 上映时间
    style = scrapy.Field()  # 制式


class NetLogItem(scrapy.Item):
    url = scrapy.Field()  # url
    urldata = scrapy.Field()  # url内容
    update = scrapy.Field()  # 创建时间


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ThreeDMConsoleGame(scrapy.Item):  # 单机游戏
    name = scrapy.Field()  # 游戏名
    publish_time = scrapy.Field()  # 发行时间
    publisher = scrapy.Field()  # 运营商
    developer = scrapy.Field()  # 开发商
    platform = scrapy.Field()  # 运营平台
    category = scrapy.Field()  # 类别  ‘单机 ***’
    language = scrapy.Field()  # 语言
    img_url = scrapy.Field()  # 图片链接
    img_path = scrapy.Field()  # 图片本地路径
    description = scrapy.Field()  # 描述
    score = scrapy.Field()  # 评分


class ThreeDMOLGame(scrapy.Item):  # 网络游戏
    name = scrapy.Field()  # 游戏名
    publish_time = scrapy.Field()  # 发行时间
    publisher = scrapy.Field()  # 运营商
    developer = scrapy.Field()  # 开发商
    state = scrapy.Field()  # 游戏状态
    category = scrapy.Field()  # 类别  ‘网游 ***’
    picture = scrapy.Field()  # 画面类型 3D等
    img_url = scrapy.Field()  # 图片链接
    img_path = scrapy.Field()  # 图片本地路径
    popularity = scrapy.Field()  # 人气
    # img_source = scrapy.Field()  # 图片数据
    label = scrapy.Field()  # 标签
    score = scrapy.Field()  # 评分


class ThreeDMShouYouGame(scrapy.Item):  # 手机游戏
    name = scrapy.Field()  # 游戏名
    publish_time = scrapy.Field()  # 发行时间
    publisher = scrapy.Field()  # 运营商
    platform = scrapy.Field()  # a1为安卓 a2为苹果
    language = scrapy.Field()  # 语言
    category = scrapy.Field()  # 类别  ‘手游 ***’
    volume = scrapy.Field()  # 游戏大小
    img_url = scrapy.Field()  # 图片链接
    img_path = scrapy.Field()  # 图片本地路径
    # img_source = scrapy.Field()  # 图片数据
    description = scrapy.Field()  # 描述
    score = scrapy.Field()  # 评分


class GameSky(scrapy.Item):
    name = scrapy.Field()  # 游戏名
    publish_time = scrapy.Field()  # 发行时间
    publisher = scrapy.Field()  # 运营商
    category = scrapy.Field()  # 类别  ‘网游 ***’
    img_url = scrapy.Field()  # 图片链接
    img_path = scrapy.Field()  # 图片本地路径
    description = scrapy.Field()  # 描述


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


class WeiboUserItem(scrapy.Item):
    """
    微博用户
    """
    user_id = scrapy.Field()  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
    nickname = scrapy.Field()  # 用户昵称，如“Dear-迪丽热巴”
    weibo_num = scrapy.Field()  # 用户全部微博数
    got_num = scrapy.Field()  # 爬取到的微博数
    following = scrapy.Field()  # 用户关注数

    followers = scrapy.Field()  # 用户粉丝数
    weibo = scrapy.Field()


class WeiboContentItem(scrapy.Item):
    """
    关系网络
    """
    user_id = scrapy.Field()  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
    weibo_content = scrapy.Field()  # 微博内容
    weibo_place = scrapy.Field()  # 微博位置
    publish_time = scrapy.Field()  # 微博发布时间
    up_num = scrapy.Field()  # 微博对应的点赞数
    retweet_num = scrapy.Field()  # 微博对应的转发数
    comment_num = scrapy.Field()  # 微博对应的评论数
    publish_tool = scrapy.Field()  # 微博发布工具


class WeiboFollowItem(scrapy.Item):
    """
    微博内容
    """
    user_id = scrapy.Field()  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
    follow_id = scrapy.Field()  # 他关注的用户ID
