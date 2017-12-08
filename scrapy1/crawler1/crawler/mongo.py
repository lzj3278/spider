# -*- coding: utf-8 -*-
r = None


class MongoTable(object):
    def __init__(self, conn, db_name, collection_name, spider_name, cache_size=100, ifcreate_table=True):
        print 'Creating Mongo Table'
        print conn
        print db_name
        print spider_name
        print collection_name
        self.conn = conn
        self.cache_size = cache_size
        self.data_cache = []
        self.db_name = db_name
        self.collection_name = collection_name
        self.spider_name = spider_name

    def insert(self, data):
        self.data_cache.append(data)
        if len(self.data_cache) > self.cache_size:
            self.flush()

    def flush(self):
        db = self.conn[self.db_name]
        cur = db[self.collection_name]
        cur.insert_many(self.data_cache)
        self.data_cache = []
