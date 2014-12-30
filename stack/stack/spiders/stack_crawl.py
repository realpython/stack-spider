from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from stack.items import StackItem


class StackSpider(CrawlSpider):
    name = "stackcrawl"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?sort=newest",
    ]
    rules = (
        Rule(
            SgmlLinkExtractor(allow=('&page=\d')),
            callback='parse',
            follow=True
        ),
    )

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        questions = hxs.xpath('//div[@class="summary"]')
        items = []
        for question in questions:
            item = StackItem()
            title = question.xpath(
                '//a[@class="question-hyperlink"]/text()').extract()
            url = question.xpath(
                '//a[@class="question-hyperlink"]/@href').extract()
            item['title'] = title
            item['url'] = url
            items.append(item)
        return items
