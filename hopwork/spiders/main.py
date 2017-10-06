# -*- coding: utf-8 -*-
import scrapy


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = ['www.hopwork.fr']
    start_urls = ['https://www.hopwork.fr/']

    def parse(self, response):
        pass
