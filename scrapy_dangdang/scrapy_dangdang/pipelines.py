# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 如果想使用管道，就必须在settings中开启管道

class ScrapyDangdangPipeline:
    # 在爬虫文件开始前就执行的方法
    def open_spider(self, spider):
        self.fp = open('book.json', 'w', encoding='utf-8')

    # item就是yield后面的book对象
    def process_item(self, item, spider):


        self.fp.write(str(item))

        return item

    # 在爬虫文件执行完之后的方法
    def close_spider(self, spider):
        self.fp.close()


import urllib.request


# 'scrapy_dangdang.pipelines.DangdangPipeline': 301,
# 多条管道开启
#   (1)定义管道类
#   (2)在settings中开启管道
class DangdangPipeline:

    def process_item(self, item, spider):
        url = 'http:' + item.get('src')
        filename = './books/' + item.get('name') + '.jpg'

        urllib.request.urlretrieve(url=url, filename=filename)

        return item
