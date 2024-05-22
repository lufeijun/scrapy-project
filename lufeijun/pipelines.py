# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
from pymysql import cursors
from twisted.enterprise import adbapi
import copy
import pymongo
from twisted.internet import reactor, defer


class LufeijunPipeline:
    def process_item(self, item, spider):
        return item

class LianjiaPipeline:
    #函数初始化
    def __init__(self, db_pool):
        self.db_pool=db_pool

    @classmethod
    def from_settings(self,settings):
        """类方法，只加载一次，数据库初始化"""
        db_params = dict(
            host="192.168.0.34",
            user="root",
            password="123456",
            port=3306,
            database="scrapy",
            charset="utf8",
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        # 返回一个pipeline对象
        return self(db_pool)

    def process_item(self, item, spider):
        myItem={}
        myItem["name"] = item["name"]
        myItem["position"] = item["position"]
        logging.warning(myItem)
        # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
        asynItem = copy.deepcopy(myItem)
        # 把要执行的sql放入连接池
        query = self.db_pool.runInteraction(self.insert_into, asynItem)

        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, myItem, spider)
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO lianjia (name,position) VALUES ('{}','{}')".format(
            item['name'], item['position'])
        # 执行sql语句
        cursor.execute(sql)
        # 错误函数
    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print("failure", failure)    


class LianjiaMongodbPipeline:

    itemList = []
    count = 100
    insertcount = 0

    def __init__(self, uri,port,db,coll,user,pwd):
        self.client = pymongo.MongoClient(host=uri)
        self.db = self.client[db]  # 获得数据库的句柄
        self.coll = self.db[coll]  # 获得collection的句柄
        # 数据库登录需要帐号密码的话
        # self.db.authenticate(user, pwd)

    @classmethod
    def from_crawler(cls, crawler):
        uri=crawler.settings.get('MONGO_HOST')
        port=crawler.settings.get('MONGO_PORT')
        db=crawler.settings.get('MONGO_DB')
        coll=crawler.settings.get('MONGO_COLL')
        user=crawler.settings.get('MONGO_USER')
        pwd=crawler.settings.get('MONGO_PSW')
        return cls(
            uri = uri,
            port = port,
            db = db,
            coll = coll,
            user = user,
            pwd = pwd
        )
    def close_spider(self, spider):
        # 批量插入，最后一步需要插入剩余的
        if len( self.itemList ) > 0 :
            self._insert_many()
        print( "总计插入条数：" , self.insertcount )
        self.client.close()

    def process_item(self, item, spider):

        # 单条插入
        # item = copy.deepcopy(item)
        # self.coll.insert_one(dict(item))
        # return item

        # 多条批量插入
        self.itemList.append( dict(item) )
        if len( self.itemList ) >= self.count:
            self._insert_many()


        # 异步插入，暂时没起作用
        # defer_out = defer.Deferred()
        # reactor.callInThread(self._insert, item, defer_out, spider)
        # yield defer_out
        # defer.returnValue(item)
    def _insert_many(self):
        self.coll.insert_many(self.itemList, ordered=False)
        self.insertcount += len( self.itemList )
        self.itemList.clear()
    # 这块好像是异步插入，没起作用
    def _insert(self, item, defer_out, spider):
        print(item)
        self.coll.insert_one(dict(item))
        reactor.callFromThread(defer_out.callback, item)