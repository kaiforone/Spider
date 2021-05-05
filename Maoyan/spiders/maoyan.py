import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset = 0

    def parse(self, response):
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
        #拼接新的url交给调度器入队列
        if self.offset <= 90:
            self.offset += 10
            url = 'https://maoyan.com/board/4?offset={}'.format(self.offset)
            #交给调度器入队列
            yield scrapy.Request(
                url = url,
                callback=self.parse
            )
