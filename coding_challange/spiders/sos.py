# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import SosItem


class SosSpider(scrapy.Spider):
    name = 'sos'
    allowed_domains = ['businesssearch.sos.ca.gov']
    start_urls = ['http://businesssearch.sos.ca.gov/']

    def start_requests(self):
        for start_url in self.start_urls:
            data = {
                    'filing':'',
                    'SearchType':'CORP',
                    'SearchCriteria':'ABC',
                    'SearchSubType':'Keyword'
                    }
            yield scrapy.FormRequest(
                url=f"{start_url}CBS/SearchResults?",
                method = 'GET',
                formdata = data,
                callback=self.parse
                )

    def parse(self, response):
        csrf = response.css('input[name=__RequestVerificationToken] ::attr(value)').get()

        detail_page_url = 'https://businesssearch.sos.ca.gov/CBS/Detail'
        entities = response.css('button[name=EntityId] ::attr(value)').getall()

        for entity in entities[:30]:
            data = {
                    '__RequestVerificationToken':csrf,
                    'SearchType': 'CORP',
                    'SearchCriteria': 'ABC',
                    'SearchSubType': 'Keyword',
                    'filing':'' ,
                    'enitityTable_length': '10',
                    'EntityId': entity
                    }
            yield scrapy.FormRequest(
                url= detail_page_url,
                formdata=data,
                callback=self.parse_entity_detail
                )

    def parse_entity_detail(self, response):
        for entity_detail in response.css('.col-md-8'):
            l = ItemLoader(selector=entity_detail, item=SosItem())
            l.add_css('entity_mailing_address', '.row:nth-child(7) .col-sm-8')
            yield l.load_item()
