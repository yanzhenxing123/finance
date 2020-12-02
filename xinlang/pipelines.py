# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import logging
import re

import pymongo
import pymysql
from pymongo import MongoClient

client = MongoClient()
collection = client['xinlang']['renrendai']

logger = logging.getLogger(__name__)
import csv

from xinlang.spiders import qs

# 保存到csv中
def save_to_csv(q: str, item: dict):
    with open('./{}.csv'.format(q), 'a+', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((item['title'],
                         item['scheme'],
                         item['created_at'],
                         item['raw_text'],
                         item['source'],))

def save_to_mongo(q: str, item: dict):
    pass


class XinlangPipeline:
    # def open_spider(self, spider):
    #     if spider.name == "renrendai":
    #         for q in qs:
    #             with open('./{}.csv'.format(q), 'a+', encoding='utf_8_sig', newline='') as f:
    #                 writer = csv.writer(f)
    #                 writer.writerow(('titil',
    #                                  'scheme',
    #                                  'created_at',
    #                                  'raw_text',
    #                                  'source',))

    def process_item(self, item, spider):
        if spider.name == "renrendai":
            # collection.insert(dict(item))
            #
            item['raw_text'] = self.process_content(item['raw_text'])

            # logger.warning(item)
            # save_to_csv(spider.q, item)

        return item

    def process_content(self, content):
        content = [re.sub(r"\u3000|\s", '', i) for i in content]
        content = [i for i in content if len(i) > 0]
        content = "".join(content)
        return content

    # def close_spider(self, spider):
    #     self.f.close()

class WeiboPipeline:

    def process_item(self, item, spider):
        if spider.name == 'weibo':
            item['created_at'] = self.process_time(item['created_at'])
            item['raw_text'] = self.process_content(item['raw_text'])
            # logger.warning(item)
            # save_to_csv(spider.q, item)
        return item

    def process_time(self, created_at):
        today = datetime.date.today()
        if '前' in created_at:
            created_at = str(today)
        elif '昨天' in created_at:
            oneday = datetime.timedelta(days=1)
            yesterday = today - oneday
            created_at = str(yesterday)
        elif len(created_at) == 5:
            date = '2020-' + created_at
            created_at = date
        return created_at

    def process_content(self, content):
        content = re.sub(r"\s", '', content)
        return content

class WdtyPipeline:
    def process_item(self, item, spider):
        if spider.name == "wdty":
            # collection.insert(dict(item))
            #
            item['raw_text'] = self.process_content(item['raw_text'])
            # logger.warning(item)
            # save_to_csv(spider.q, item)
        return item

    def process_content(self, content):
        content = [re.sub(r"\\xa0|\s", '', i) for i in content]
        content = [i for i in content if len(i) > 0]
        content = "".join(content)
        return content


class MongoPipline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.client.admin.authenticate("admin", "123456")

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''

        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        item['insert_time'] = str(otherStyleTime)
        data = dict(item)
        collection = spider.q
        table = self.db[collection]
        table.insert_one(data)
        return item


class MysqlPipeline:
    def __init__(self, mysql_host, mysql_port, mysql_db, mysql_user, mysql_password):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''

        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_db=crawler.settings.get('MYSQL_DB'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''

        self.connect = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            passwd=self.mysql_password,
            db=self.mysql_db
        )
        self.cursor = self.connect.cursor()

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.connect.close()
        self.cursor.close()

    def process_item(self, item, spider):
        '''
            每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
        '''

        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        item['insert_time'] = str(otherStyleTime)
        item['platform'] = str(spider.q)
        self.insert_data('article', item)
        return item

    def insert_data(self, table_name, item):
        try:
            insert_sql = '''
                    insert into `%s` (title, scheme, raw_text, source, created_at, insert_time, platform) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');
                    ''' % (
                table_name,
                item['title'],
                item['scheme'],
                item['raw_text'],
                item['source'],
                item['created_at'],
                item['insert_time'],
                item['platform'],
            )
            self.cursor.execute(insert_sql)

        except Exception as e:
            print(e,'****')
        self.connect.commit()




