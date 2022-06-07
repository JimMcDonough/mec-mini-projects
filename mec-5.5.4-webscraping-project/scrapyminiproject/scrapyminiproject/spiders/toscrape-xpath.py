# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:46:44 2022

@author: jimmc
"""
import scrapy

class QuotesSpider(scrapy.Spider):   
    name = "toscrape-xpath"
    
    start_urls = [
               'http://quotes.toscrape.com/page/1/',
           ]
    
    def parse(self, response):
        for quote in response.xpath("//div[@class = 'quote']"):
            yield {
                'text': quote.xpath(".//span[@class = 'text']/text()").get(),
                'author': quote.xpath(".//span/small[@class = 'author']/text()").get(),
                'tags': quote.xpath(".//div[@class = 'tags']/a[@class = 'tag']/text()").getall(),
            }
        try:   
            next_page = response.xpath("//li[@class = 'next']/a").attrib['href']
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass