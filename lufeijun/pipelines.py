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