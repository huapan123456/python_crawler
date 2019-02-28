# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp_spider.items import WxappItem
from scrapy.http.response.html import HtmlResponse

class WxappSpider(CrawlSpider):
    name = 'wxapp'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=1&page=1']

    rules = (
        Rule(LinkExtractor(allow=r".+mod=list&catid=1&page=\d"),follow=True),
        Rule(LinkExtractor(allow=r'.+article-.*'), callback='parse_detail', follow=False)
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='ph']/text()").extract_first()
        time = response.xpath("//span[@class='time']/text()").extract_first()
        content = response.xpath("//div[contains(@class,'content_middle')]//div[@class='d']//text()").extract()
        item = WxappItem(title=title,time=time,content=content)
        yield item
