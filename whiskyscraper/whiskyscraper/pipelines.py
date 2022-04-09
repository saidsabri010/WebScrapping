# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class WhiskyscraperPipeline:
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'said'
        database = 'student'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,
            dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute("""insert into data_rooms values(%s,%s,%s,%s,%s)""",
                             (item['url'][0], item['city'][0], item['roomType'][0], item['rentPrice'][0],
                              item['surfaceSize'][0]))
            self.connection.commit()
        except:
            self.connection.rollback()
        return item
