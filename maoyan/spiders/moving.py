# -*- coding: utf-8 -*-
import scrapy

from maoyan.items import MaoyanItem


class MovingSpider(scrapy.Spider):
    name = 'moving'
    allowed_domains = ['maoyao.com']
    start_urls = ['http://maoyan.com/board/4']

    def parse(self, response):
        results = response.selector.css('.movie-item-info a::text').extract()
        for result in results:
            item = MaoyanItem()
            item['title'] = result
            # item['star'] = result.css('.start::text').extract_first()
            # item['releasetime'] = result.css('.releasetime::text').extract_first()
            yield item
        next = response.css('.list-pager a::attr(href)').extract()[-1]
        print('*' * 20)
        print(next)

        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)




