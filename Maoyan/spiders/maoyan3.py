import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan3'
    allowed_domains = ['maoyan.com']

    #重写start_requests()方法，把URL地址一次交给调度器
    def start_requests(self):
        for offset in range(0,91,10):
            url = 'https://maoyan.com/board/4?offset={}'.format(offset)
            yield scrapy.Request(
                url=url,
                callback=self.parse_html
            )

    def parse_html(self,response):
        #基准xpath
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        #遍历取数据
        for dd in dd_list:
            #创建对象
            item = MaoyanItem()
            #取出数据，赋值给item对象
            item['name'] = dd.xpath('./a/@title').get().strip()
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract_first().strip()
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').get().strip()
            #把爬取的数据交给管道文件pipline处理
            yield item
