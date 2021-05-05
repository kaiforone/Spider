# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from .settings import  *

class MaoyanPipeline:
    def process_item(self, item, spider):
        print(item['name'],item['time'])
        return item


#定义一个mysql管道类
class MaoyanMysqlPipeline:
    def open_spider(self,spider):
        #爬虫程序启动时，只执行一次，一般用于建立数据库链接
        self.db = pymysql.connect(
            host = MYSQL_HOST,
            user = MYSQL_USER,
            password = MYSQL_PWD,
            database = MYSQL_DB,
            charset = MYSQL_CHAR
        )
        self.cursor = self.db.cursor()
        print('open')

    def process_item(self,item,spider):
        #插入数据到mysql
        ins = 'insert into filmtab VALUES (%s,%s,%s)'
        film_list = [
            item['name'],item['star'],item['time']
        ]
        self.cursor.execute(ins,film_list)
        self.db.commit()
        return item

    def close_spider(self,spider):
        #爬虫程序结束时，只执行一次，一般用于关闭数据库链接
        self.cursor.close()
        self.db.close()
        print('close')
