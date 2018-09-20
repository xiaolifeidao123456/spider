# -*- coding: utf-8 -*-
import scrapy
import json
from qicha.agent_helper import get_random_agent
from qicha.items import QichaItem

class CompanySpider(scrapy.Spider):
    name = 'company'
    allowed_domains = ['www.qichamao.com']
    start_urls = ['http://www.qichamao.com/']

    def start_requests(self):
        data = {'pagesize': '9'}
        base_url = 'https://www.qichamao.com/cert-wall'
        agent = get_random_agent()
        print(agent)

        headers = {
            'Referer': 'https://www.qichamao.com/cert-wall/',
            'User-Agent': agent,
            'Host': 'www.qichamao.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
        }

        for page in range(2, self.settings.get('MAX_PAGE') + 1):
            print('*' * 20)
            print(page)
            data['page'] = str(page)

            yield scrapy.FormRequest(url = base_url,
                         headers = headers,
                         method = 'POST',             
                         formdata = data,       
                         callback = self.parse,
                         )

    def parse(self, response):
        result = json.loads(response.text)
        for data in result.get('dataList'):
            item = QichaItem()
            item['company_name'] = data.get('CompanyName')
            item['c_phone'] = data.get('c_phone')
            yield item
