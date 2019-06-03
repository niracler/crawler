# -*- coding: utf-8 -*-

from random import random
import json
import random
import re
import sys
import traceback
from datetime import datetime
from datetime import timedelta
from time import sleep
import requests
import scrapy
from lxml import etree
from scrapy_redis.spiders import RedisCrawlSpider
from tqdm import tqdm
from crawler.items import WeiboUserItem


class Weibo(RedisCrawlSpider):
    name = 'weibo_redis'
    allowed_domains = ['weibo.cn']
    redis_key = 'weibo:start_urls'
    # start_urls = ['https://weibo.cn/u/5829543885']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter = 1
        self.got_num = 0  # 爬取到的微博数
        self.weibo = []
        itemDict = {}
        try:
            with open('cookie.json') as f:
                self.cookie_json = json.loads(f.read())
        except:
            self.cookie = {}

        items = self.cookie_json['Cookie'].split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        self.cookie = itemDict

        print(self.cookie)

    def make_requests_from_url(self, url):
        cookie = self.cookie
        headers = {
            'Connection': 'keep - alive',
            'User-Agent': self.cookie_json["user-agent"]
        }
        return scrapy.Request(url=url, headers=headers, cookies=cookie)

    def parse(self, response):
        item = WeiboUserItem()
        self.user_id = int(response.url.split('/')[-1])
        item['user_id'] = self.user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        item['nickname'] = response.xpath("//title/text()").extract_first()[0:-3]  # 用户昵称，如“Dear-迪丽热巴”

        user_info = response.xpath("//div[@class='tip2']/*/text()").extract()

        item['weibo_num'] = int(user_info[0][3:-1])  # 用户全部微博数
        item['following'] = int(user_info[1][3:-1])  # 用户关注数
        item['followers'] = int(user_info[2][3:-1])  # 用户粉丝数

        page_num = self.get_page_num(response)  # 获取微博总页数
        print(page_num)
        page1 = 0
        random_pages = random.randint(1, 5)
        for page in tqdm(range(1, page_num + 1), desc=u"进度"):
            self.get_one_page(page)  # 获取第page页的全部微博

            # 通过加入随机等待避免被限制。爬虫速度过快容易被系统限制(一段时间后限
            # 制会自动解除)，加入随机等待模拟人的操作，可降低被系统限制的风险。默
            # 认是每爬取1到5页随机等待6到10秒，如果仍然被限，可适当增加sleep时间
            if page - page1 == random_pages:
                sleep(random.randint(6, 10))
                page1 = page
                random_pages = random.randint(1, 5)

        if not self.filter:
            print(u"共爬取" + str(self.got_num) + u"条微博")
        else:
            print(u"共爬取" + str(self.got_num) + u"条原创微博")

        item['got_num'] = self.got_num  # 爬取到的微博数
        item['weibo'] = self.weibo

        yield item

    def get_page_num(self, response):
        """获取微博总页数"""
        try:
            if response.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(
                    response.xpath("//input[@name='mp']")[0].attrib["value"])
            return page_num
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_one_page(self, page):
        """获取第page页的全部微博"""
        try:
            url = "https://weibo.cn/u/%d?page=%d" % (self.user_id, page)
            selector = self.deal_html(url)
            info = selector.xpath("//div[@class='c']")
            is_empty = info[0].xpath("div/span[@class='ctt']")
            if is_empty:
                for i in range(0, len(info) - 2):
                    is_retweet = info[i].xpath("div/span[@class='cmt']")
                    if (not self.filter) or (not is_retweet):
                        self.weibo.append({})
                        self.get_weibo_content(info[i])  # 微博内容
                        self.get_weibo_place(info[i])  # 微博位置
                        self.get_publish_time(info[i])  # 微博发布时间
                        self.get_publish_tool(info[i])  # 微博发布工具
                        self.get_weibo_footer(info[i])  # 微博点赞数、转发数、评论数
                        self.got_num += 1
                        print("-" * 100)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def deal_html(self, url):
        """处理html"""
        try:
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            return selector
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def deal_garbled(self, info):
        """处理乱码"""
        try:
            info = info.xpath(
                "string(.)").replace(u"\u200b", "").encode(sys.stdout.encoding, "ignore").decode(
                sys.stdout.encoding)
            return info
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_long_weibo(self, weibo_link):
        """获取长原创微博"""
        try:
            selector = self.deal_html(weibo_link)
            info = selector.xpath("//div[@class='c']")[1]
            wb_content = self.deal_garbled(info)
            wb_time = info.xpath("//span[@class='ct']/text()")[0]
            wb_content = wb_content[wb_content.find(
                ":") + 1:wb_content.rfind(wb_time)]
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_original_weibo(self, info):
        """获取原创微博"""
        try:
            weibo_content = self.deal_garbled(info)
            weibo_content = weibo_content[:weibo_content.rfind(u"赞")]
            a_text = info.xpath("div//a/text()")
            if u"全文" in a_text:
                weibo_id = info.xpath("@id")[0][2:]
                weibo_link = "https://weibo.cn/comment/" + weibo_id
                wb_content = self.get_long_weibo(weibo_link)
                if wb_content:
                    weibo_content = wb_content
            return weibo_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_long_retweet(self, weibo_link):
        """获取长转发微博"""
        try:
            wb_content = self.get_long_weibo(weibo_link)
            wb_content = wb_content[:wb_content.rfind(u"原文转发")]
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_retweet(self, info):
        """获取转发微博"""
        try:
            original_user = info.xpath("div/span[@class='cmt']/a/text()")
            if not original_user:
                wb_content = u"转发微博已被删除"
                return wb_content
            else:
                original_user = original_user[0]
            wb_content = self.deal_garbled(info)
            wb_content = wb_content[wb_content.find(
                ":") + 1:wb_content.rfind(u"赞")]
            wb_content = wb_content[:wb_content.rfind(u"赞")]
            a_text = info.xpath("div//a/text()")
            if u"全文" in a_text:
                weibo_id = info.xpath("@id")[0][2:]
                weibo_link = "https://weibo.cn/comment/" + weibo_id
                wb_content = self.get_long_retweet(weibo_link)
                if wb_content:
                    weibo_content = wb_content
            retweet_reason = self.deal_garbled(info.xpath("div")[-1])
            retweet_reason = retweet_reason[:retweet_reason.rindex(u"赞")]
            wb_content = (retweet_reason + "\n" + u"原始用户: " +
                          original_user + "\n" + u"转发内容: " + wb_content)
            return wb_content
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_weibo_content(self, info):
        """获取微博内容"""
        try:
            is_retweet = info.xpath("div/span[@class='cmt']")
            if is_retweet:
                weibo_content = self.get_retweet(info)
            else:
                weibo_content = self.get_original_weibo(info)
            self.weibo[-1]['weibo_content'] = weibo_content
            print(weibo_content)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_weibo_place(self, info):
        """获取微博发布位置"""
        try:
            div_first = info.xpath("div")[0]
            a_list = div_first.xpath("a")
            weibo_place = u"无"
            for a in a_list:
                if ("place.weibo.com" in a.xpath("@href")[0] and
                        a.xpath("text()")[0] == u"显示地图"):
                    weibo_a = div_first.xpath("span[@class='ctt']/a")
                    if len(weibo_a) >= 1:
                        weibo_place = weibo_a[-1]
                        if u"视频" == div_first.xpath("span[@class='ctt']/a/text()")[-1][-2:]:
                            if len(weibo_a) >= 2:
                                weibo_place = weibo_a[-2]
                            else:
                                weibo_place = u"无"
                        weibo_place = self.deal_garbled(weibo_place)
                        break
            self.weibo[-1]['weibo_place'] = weibo_place
            print(u"微博位置: " + weibo_place)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_publish_time(self, info):
        """获取微博发布时间"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.deal_garbled(str_time[0])
            publish_time = str_time.split(u'来自')[0]
            if u"刚刚" in publish_time:
                publish_time = datetime.now().strftime(
                    '%Y-%m-%d %H:%M')
            elif u"分钟" in publish_time:
                minute = publish_time[:publish_time.find(u"分钟")]
                minute = timedelta(minutes=int(minute))
                publish_time = (datetime.now() - minute).strftime(
                    "%Y-%m-%d %H:%M")
            elif u"今天" in publish_time:
                today = datetime.now().strftime("%Y-%m-%d")
                time = publish_time[3:]
                publish_time = today + " " + time
            elif u"月" in publish_time:
                year = datetime.now().strftime("%Y")
                month = publish_time[0:2]
                day = publish_time[3:5]
                time = publish_time[7:12]
                publish_time = (year + "-" + month + "-" + day + " " + time)
            else:
                publish_time = publish_time[:16]
            self.weibo[-1]['publish_time'] = publish_time
            print(u"微博发布时间: " + publish_time)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_publish_tool(self, info):
        """获取微博发布工具"""
        try:
            str_time = info.xpath("div/span[@class='ct']")
            str_time = self.deal_garbled(str_time[0])
            if len(str_time.split(u'来自')) > 1:
                publish_tool = str_time.split(u'来自')[1]
            else:
                publish_tool = u"无"
            self.weibo[-1]['publish_tool'] = publish_tool
            print(u"微博发布工具: " + publish_tool)
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_weibo_footer(self, info):
        """获取微博点赞数、转发数、评论数"""
        try:
            pattern = r"\d+"
            str_footer = info.xpath("div")[-1]
            str_footer = self.deal_garbled(str_footer)
            str_footer = str_footer[str_footer.rfind(u'赞'):]
            weibo_footer = re.findall(pattern, str_footer, re.M)

            up_num = int(weibo_footer[0])
            self.weibo[-1]['up_num'] = up_num
            print(u"点赞数: " + str(up_num))

            retweet_num = int(weibo_footer[1])
            self.weibo[-1]['retweet_num'] = retweet_num
            print(u"转发数: " + str(retweet_num))

            comment_num = int(weibo_footer[2])
            self.weibo[-1]['comment_num'] = comment_num
            print(u"评论数: " + str(comment_num))
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()
