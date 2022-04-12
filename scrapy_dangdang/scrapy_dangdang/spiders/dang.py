import scrapy

from scrapy_dangdang.items import ScrapyDangdangItem


class DangSpider(scrapy.Spider):
    name = 'dang'
    #如果是多页下载的话，必须调整allowed_domains的范围，一般情况下只写域名
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.01.00.00.00.00.html']

    base_url = 'http://category.dangdang.com/pg'

    page = 1

    def parse(self, response):

        # piplines  下载数据
        # items      定义数据结构
        # src = //ul[@id="component_59"]/li//img/@src
        # name = //ul[@id="component_59"]/li//img/@alt
        # price = //ul[@id="component_59"]/li/p[@class = "price"]/span[1]/text()

        li_list = response.xpath('//ul[@id="component_59"]/li')
        # 所有的selector对象都可以再次调用XPATH方法,类似于相对路径
        for li in li_list:
            # 第一张图片没有使用懒加载
            # 所以第一张图片和其他图片的标签属性是不一样的。
            # 第一张图片的src是可以使用的，
            # 其他图片因为懒加载，所以使用data-original
            src = li.xpath('.//img/@data-original').extract_first()

            if src:
                src = src
            else:
                src = li.xpath('.//img/@src').extract_first()

            name = li.xpath('.//img/@alt').extract_first()
            price = li.xpath('./p[@class = "price"]/span[1]/text()').extract_first()
            book = ScrapyDangdangItem(src=src, name=name, price=price)
            #获取一个book就将book交给pipelines
            yield book

    #每一页爬取的业务逻辑都是一样的，只需要更换页码再次调用parse()方法即可
            if self.page < 100:
                self.page = self.page + 1

                url = self.base_url + str(self.page) + '-cp01.01.00.00.00.00.html'

                #怎么调用parse方法
                #scrapy.Request是scrapy的get请求
                #url就是请求地址
                #callback是要执行的函数
                yield scrapy.Request(url=url,callback=self.parse)