from typing import Iterable
import scrapy

from lufeijun.items import LianjiaItem

# 
class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://bj.lianjia.com/ershoufang/"]

    # https://bj.lianjia.com/ershoufang/pg1/
    def start_requests(self):
      for i in range(1,101):
        url = "https://bj.lianjia.com/ershoufang/pg"+ repr(i) +"/"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        liList = response.xpath('//*[@id="content"]/div[1]/ul/li')
        # print( len(liList) )
        for li in liList:
            title = li.xpath('.//div[@class="title"]/a[1]/text()').extract_first()
            url = li.xpath('.//div[@class="title"]/a[1]//@href').extract_first()
            address = li.xpath(".//div[@class='positionInfo']/a[1]/text()").extract_first()
            address_region = li.xpath(".//div[@class='positionInfo']/a[2]/text()").extract_first()
            house_msg = li.xpath(".//div[@class='address']/div[1]/text()").extract_first()
            star_msg = li.xpath(".//div[@class='followInfo']/text()").extract_first()
            tag = li.xpath(".//div[@class='tag']/span/text()").extract()
            total = li.xpath(".//div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/span[1]/text()").extract_first()
            price = li.xpath(".//div[@class='priceInfo']/div[@class='unitPrice']/@data-price").extract_first()

            if not title :
                continue

            item = LianjiaItem(
                title = title.strip(),
                url = url.strip(),
                address = address.strip(),
                address_region = address_region.strip(),
                house_msg = house_msg.strip(),
                star_msg = star_msg.strip(),
                tag = tag,
                total = float(total.strip()),
                price = float(price.strip())
            )
            yield item