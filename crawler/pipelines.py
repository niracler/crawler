# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests

from sqlalchemy.orm import sessionmaker

from crawler.tool import sftp_upload


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class GamePipeline(object):
    def process_item(self, item, spider):
        data = {
            "img_path": item["img_path"],
            "name": item["name"],
            "publish_time": item["publish_time"]
        }

        url = "http://127.0.0.1:8001/api/v1/game"
        r = requests.post(url, json=data)
        if r.status_code != 201:
            print(r.text)
        return item

class ArticlePipeline(object):
    def process_item(self, item, spider):
        data = {
            "title": item['title'],
            "content": item['content'],
            "url": item['url'],
            'website_name': item['website'],
            'publish_time': item['publish_time']
        }

        url = "http://127.0.0.1:8000/api/article/"
        r = requests.post(url, data=data)
        if r.status_code != 201:
            print(r.text)
        return item


class ImgDownloadPipeline(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }

    def process_item(self, item, spider):
        img_url = item['img_url']
        img_path = item['img_path']

        with open('/home/niracler/work/media' + img_path, 'wb') as f:
            f.write(requests.get(url=img_url, headers=self.headers).content)

        return item
