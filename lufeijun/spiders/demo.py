import scrapy

from lufeijun.items import LufeijunItem

# 在执行 scrapy crawl demo 开始爬取后，所有中间件中的 spider 参数，就是指的这个类

class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["www.baidu.com"]
    start_urls = [
        "https://www.baidu.com/",
        "https://www.youdao.com/",
    ]

    def parse(self, response):
        item = LufeijunItem()
        item["name"] = "姓名"
        yield item

    def sayHello(self):
        print("hello world")    
