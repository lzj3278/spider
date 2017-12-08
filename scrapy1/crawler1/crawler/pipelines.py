import sys

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.exceptions import DropItem

from mongo import MongoTable


class CheckPipeline(object):
    def process_item(self, item, spider):
        for key in item:
            if item[key] is None:
                raise DropItem('%s is missing %s' % (item, key))
        return item


class EncodingPipeline(object):
    def process_item(self, item, spider):
        for key in item:
            item[key] = item[key].encode('utf-8')
        return item


# class MySQLPipeline(object):
#     def __init__(self, host, username, password, db):
#         self.host = host
#         self.username = username
#         self.password = password
#         self.db = db
#
#     def process_item(self, item, spider):
#         try:
#             self.table.insert(item['mall'], item['rank'], item['title'], item['price'],
#                               item['turnover_index'], item['top_id'], item['type_id1'], item['type_id2'], item['url'])
#         except Exception as e:
#             pass
#
#         return item
#
#     @classmethod
#     def from_settings(cls, settings):
#         host = settings['MYSQL_HOST']
#         username = settings['MYSQL_USERNAME']
#         password = settings['MYSQL_PASSWORD']
#         db = settings['MYSQL_DB']
#         return cls(host, username, password, db)
#
#     def open_spider(self, spider):
#         import MySQLdb
#         # create_table is default true
#
#         self.conn = MySQLdb.connect(self.host, self.username,
#                                     self.password, self.db, charset='utf8')
#         self.table = good_Table(self.conn, spider.name, cache_size=100)
#
#     def close_spider(self, spider):
#         self.table.flush()
#         self.conn.close()

class MongoPipeline(object):
    def __init__(self, host, port, db, collection):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection

    def process_item(self, item, spider):
        try:
            data = {
                'mall': item['mall'],
                'rank': item['rank'],
                'title': item['title'],
                'top_id': item['top_id'],
                'type_id1': item['type_id1'],
                'type_id2': item['type_id2'],
                'url': item['url']}
            self.table.insert(data)
        except Exception as e:
            print e

        return item

    @classmethod
    def from_settings(cls, settings):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        db = settings['MONGO_DB']
        collection = settings['MONGO_COLLECTION']
        return cls(host, port, db, collection)

    def open_spider(self, spider):
        from pymongo import MongoClient

        self.conn = MongoClient(host=self.host, port=self.port)
        self.table = MongoTable(self.conn, self.db, self.collection, spider.name, cache_size=100)

    def close_spider(self, spider):
        self.table.flush()
        self.conn.close()
