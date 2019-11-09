# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests

from sqlalchemy.orm import sessionmaker
from .models import Movie, db_connect, create_table, MovieBoxOffice

from crawler.tool import sftp_upload


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class MoviePipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
        Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()

        movie = Movie()

        movie.ranking = int(item['ranking'])
        movie.mid = int(item['mid'])
        movie.name = item['name']
        movie.english_name = item['english_name']
        movie.release_year = item['release_year']
        movie.default_image = item['default_image']
        movie.style = item['style']
        movie.release_time = item['release_time']
        movie.duration = item['duration']
        movie.movie_type = item['movie_type']
        movie.director = item['director']
        movie.starring = item['starring']
        movie.production_company = item['production_company']
        movie.publish_company = item['publish_company']

        try:
            movie.box_office = int(item['box_office'])
        except ValueError:
            print('box_office: ' + item['box_office'])
            movie.box_office = 0

        movie.area = item['area']
        movie.area_id = int(item['area_id'])

        mbolist = []
        for i in range(len(item['week'])):
            movie_box_office = MovieBoxOffice()
            movie_box_office.mid_id = movie.mid
            movie_box_office.week = item['week'][i]
            movie_box_office.week_time = item['week_time'][i]
            movie_box_office.average_per_game = item['average_per_game'][i]
            movie_box_office.one_week_box_office = item['one_week_box_office'][i]
            movie_box_office.total_box_office = item['total_box_office'][i]
            movie_box_office.days_released = item['days_released'][i]

            mbolist.append(movie_box_office)

        try:
            session.add(movie)
            session.commit()

            for mbo in mbolist:
                session.add(mbo)

            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_SERVER'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        if spider.custom_settings and spider.custom_settings.get('MONGODB_COLLECTION'):
            self.collection = spider.custom_settings.get('MONGODB_COLLECTION')
        else:
            self.collection = spider.settings['MONGODB_COLLECTION']
        self.db[self.collection].create_index(spider.item_index, unique=True)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item


class ImgDownloadPipeline(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }

    def process_item(self, item, spider):
        img_url = item['img_url']
        img_path = item['img_path']

        with open('.' + img_path, 'wb') as f:
            f.write(requests.get(url=img_url, headers=self.headers).content)

        host = 'test.niracler.com'  # 主机
        port = 22  # 端口
        username = 'niracler'  # 用户名
        password = '159258'  # 密码
        local = '.' + img_path  # 本地文件或目录，与远程一致，当前为windows目录格式，window目录中间需要使用双斜线
        remote = '/home/niracler/PycharmProjects/display-back-end' + img_path  # 远程文件或目录，与本地一致，当前为linux目录格式
        sftp_upload(host, port, username, password, local, remote)  # 上传

        return item
