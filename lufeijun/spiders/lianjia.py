import scrapy

from lufeijun.items import LianjiaItem

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://bj.lianjia.com/ershoufang/"]

    def parse(self, response):
        liList = response.xpath('//*[@id="content"]/div[1]/ul/li')
        print( len( liList ) )
        for li in liList:
            name = li.xpath('.//div[@class="title"]/a[1]/text()').extract_first()
            position = li.xpath(".//div[@class='positionInfo']/a[1]/text()").extract_first()
            item = LianjiaItem(name=name,position=position)
            yield item
