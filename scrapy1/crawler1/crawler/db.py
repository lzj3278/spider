# -*- coding: utf-8 -*-
r=None

class Table(object):
    def __init__(self,conn,cache_size=100,ifcreate_table=True):
        self.conn = conn
        self.cache_size = cache_size
        self.data_cache=[]

        cur=self.conn.cursor()
        if ifcreate_table:
            cur.execute(self.create_stmt)
        conn.commit()

    def insert(self,*args):
        self.data_cache.append(args)
        if len(self.data_cache)>self.cache_size:
            self.flush()

    def flush(self):
        cur=self.conn.cursor()
        cur.executemany(self.insert_stmt,self.data_cache)
        self.conn.commit()
        self.data_cache=[]

class good_Table(Table):
    def __init__(self,conn,spider_name,cache_size=100,ifcreate_table=True):
        self.table_name='good_info'
        self.create_stmt='CREATE TABLE IF NOT EXISTS '\
                         +self.table_name+'(`id` int(11) not null auto_increment,`mall` int, `rank` int,`title` VARCHAR(250) NOT NULL,' \
                                          '`top_id` VARCHAR(200),`type_id1` VARCHAR(200), `type_id2` VARCHAr(200),' \
                                          '`url` VARCHAR(200), PRIMARY KEY(id));'
        self.insert_stmt='INSERT INTO '+self.table_name+' VALUES(NULL, %s, %s, %s, %s,  %s, %s, %s);'
        Table.__init__(self,conn,cache_size=cache_size,ifcreate_table=ifcreate_table)
