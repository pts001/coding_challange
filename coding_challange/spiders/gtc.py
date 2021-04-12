# -*- coding: utf-8 -*-
import re
import scrapy
import json
from scrapy.loader import ItemLoader
from ..items import GtcItems
from scrapy.http import TextResponse


class GtcSpider(scrapy.Spider):
    name = 'gtc'
    allowed_domains = ['gtc.dor.ga.gov']
    start_urls = ['http://gtc.dor.ga.gov/']

    headers ={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            }
    #
    start_urls = ['https://gtc.dor.ga.gov/_/#1']
    #
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url = url,
                headers = self.headers,
                callback = self.load_data,
                dont_filter = True
            )

    def load_data(self, response):
        response_headers = response.headers
        header_dict = response_headers.to_unicode_dict()
        fast_rw = header_dict['fast-ver-source'].replace('_:','').split(' @ ')
        fast_ver_source = f'_:[{fast_rw[0]}] @ {fast_rw[1]}'
        data = {
                'Load': '1',
                'FAST_SCRIPT_VER__': '1',
                'FAST_VERLAST__': header_dict['Fast-Ver-Last'],
                'FAST_VERLAST_SOURCE__': f'HTML:{fast_ver_source}',
                'FAST_CLIENT_WINDOW__': 'FWDC.WND-610c-39e3-d86e',
                'FAST_CLIENT_AJAX_ID__': '1',
                'FAST_CLIENT_TRIGGER__': 'InitPage'
        }

        yield scrapy.FormRequest(
            url = 'https://gtc.dor.ga.gov/_/',
            formdata = data,
            method = 'GET',
            callback = self.navigate_licence
        )

    def navigate_licence(self, response):
        response_headers = response.headers
        header_dict = response_headers.to_unicode_dict()


        data = {
                'LASTFOCUSFIELD__': 'l_r-1-4',
                'DOC_MODAL_ID__': '0',
                'EVENT__': 'r-1-4',
                'TYPE__': '0',
                'CLOSECONFIRMED__': 'false',
                'FAST_SCRIPT_VER__': '1',
                'FAST_VERLAST__': header_dict['Fast-Ver-Last'],
                'FAST_VERLAST_SOURCE__': header_dict['Fast-Ver-Source'],
                'FAST_CLIENT_WINDOW__': 'FWDC.WND-610c-39e3-d86e',
                'FAST_CLIENT_AJAX_ID__': '3',
                'FAST_CLIENT_TRIGGER__': 'DocFieldLinkClick',
                'FAST_CLIENT_SOURCE_ID__':' r-1-4'
            }

        yield scrapy.FormRequest(
            url = 'https://gtc.dor.ga.gov/_/EventOccurred',
            headers = self.headers,
            formdata = data,
            method = 'POST',
            callback = self.enter_name
        )

    def enter_name(self, response):
        response_headers = response.headers
        header_dict = response_headers.to_unicode_dict()
        data = {
                'd-h': 'A',
                'LASTFOCUSFIELD__': 'd-h',
                'DOC_MODAL_ID__': '0',
                'FAST_SCRIPT_VER__': '1',
                'FAST_VERLAST__': header_dict['Fast-Ver-Last'],
                'FAST_VERLAST_SOURCE__': header_dict['Fast-Ver-Source'],
                'FAST_CLIENT_WINDOW__': 'FWDC.WND-610c-39e3-d86e',
                'FAST_CLIENT_AJAX_ID__': '4',
                'FAST_CLIENT_TRIGGER__': 'Events.Field.blur',
                'FAST_CLIENT_SOURCE_ID__':' d-h'
            }

        yield scrapy.FormRequest(
            url = 'https://gtc.dor.ga.gov/_/Recalc',
            headers = self.headers,
            formdata = data,
            method = 'POST',
            callback = self.select_mfdl
        )

    def select_mfdl(self, response):
        response_headers = response.headers
        header_dict = response_headers.to_unicode_dict()
        data = {
                'd-b':' LICMFD',
                'd-h': 'A',
                'LASTFOCUSFIELD__': 'd-b_1',
                'DOC_MODAL_ID__': '0',
                'FAST_SCRIPT_VER__': '1',
                'FAST_VERLAST__': header_dict['Fast-Ver-Last'],
                'FAST_VERLAST_SOURCE__': header_dict['Fast-Ver-Source'],
                'FAST_CLIENT_WINDOW__': 'FWDC.WND-610c-39e3-d86e',
                'FAST_CLIENT_AJAX_ID__': '5',
                'FAST_CLIENT_TRIGGER__': 'CheckboxChange',
                'FAST_CLIENT_SOURCE_ID__': 'd-b_1'
            }

        yield scrapy.FormRequest(
            url = 'https://gtc.dor.ga.gov/_/Recalc',
            headers = self.headers,
            formdata = data,
            method = 'POST',
            callback = self.form_submit
        )

    def form_submit(self, response):
        response_headers = response.headers
        header_dict = response_headers.to_unicode_dict()
        data = {
            'd-b': 'LICMFD',
            'd-h': 'A',
            'LASTFOCUSFIELD__': 'd-k',
            'DOC_MODAL_ID__': '0',
            'EVENT__': 'd-k',
            'TYPE__': '0',
            'CLOSECONFIRMED__': 'false',
            'FAST_VERLAST__': header_dict['Fast-Ver-Last'],
            'FAST_VERLAST_SOURCE__': header_dict['Fast-Ver-Source'],
            'FAST_CLIENT_WINDOW__': 'FWDC.WND-610c-39e3-d86e',
            'FAST_CLIENT_AJAX_ID__': '6',
            'FAST_CLIENT_TRIGGER__': 'DocFieldLinkClick',
            'FAST_CLIENT_SOURCE_ID__': 'd-k'
        }
        yield scrapy.FormRequest(
            url = 'https://gtc.dor.ga.gov/_/EventOccurred',
            headers = self.headers,
            formdata = data,
            method = 'POST',
            callback = self.fetch_details
            )

    def fetch_details(self, response):
        response_headers = response.headers
        header_dict = response_headers.to_unicode_dict()
        data = {
            'd-b': 'LICMFD',
            'd-h': 'A',
            'LASTFOCUSFIELD__': 'l_d-31-1',
            'DOC_MODAL_ID__': '0',
            'EVENT__': 'd-31-1',
            'TYPE__': '0',
            'CLOSECONFIRMED__': 'false',
            'FAST_VERLAST__': header_dict['Fast-Ver-Last'],
            'FAST_VERLAST_SOURCE__': header_dict['Fast-Ver-Source'],
            'FAST_CLIENT_WINDOW__': 'FWDC.WND-610c-39e3-d86e',
            'FAST_CLIENT_AJAX_ID__': '7',
            'FAST_CLIENT_TRIGGER__': 'DocFieldLinkClick',
            'FAST_CLIENT_SOURCE_ID__': 'd-31-1'
        }
        yield scrapy.FormRequest(
            url = 'https://gtc.dor.ga.gov/_/EventOccurred',
            headers = self.headers,
            formdata = data,
            method = 'POST',
            callback = self.parse_details
            )

    def parse_details(self, response):
        json_response = response.json()
        html_text = json_response['html']

        l = ItemLoader(item =GtcItems())
        l.add_value('name', re.search(r'Name\:\s?\t+[A-Za-z0-9,.)( ]+',html_text).group())
        l.add_value('address', re.search(r'Address\:\s?\t+[A-Za-z0-9,.#)( -]+',html_text).group())
        l.add_value('reg_yr', re.search(r'Registration Year\:\s?\t+[0-9/]+',html_text).group())
        l.add_value('license_no', re.search(r'License Number\:\s?\t+[A-Z0-9 ]+',html_text).group())
        l.add_value('license_type' ,re.search(r'License Type\:\s?\t+[A-Za-z -]+',html_text).group())
        l.add_value('ownership_type',re.search(r'Ownership Type\:\s?\t+[A-Za-z]+',html_text).group())
        l.add_value('status', re.search(r'Status\:\s?\t+[A-Za-z]+',html_text).group())
        l.add_value('county', re.search(r'County\:\s?\t+[A-Za-z ]+',html_text).group())
        l.add_value('effective_date', re.search(r'Effective Date\:\s?\t+[0-9/]+',html_text).group())

        yield l.load_item()
