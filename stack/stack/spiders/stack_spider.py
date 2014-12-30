from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]')

        for question in questions:
            item = StackItem()
            title = question.xpath(
                '//a[@class="question-hyperlink"]/text()').extract()
            url = question.xpath(
                '//a[@class="question-hyperlink"]/@href').extract()
            item['title'] = title
            item['url'] = url

        return item
