import scrapy


class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["demo.com"]
    start_urls = ["http://demo.com"]

    def parse(self, response):
        pass
