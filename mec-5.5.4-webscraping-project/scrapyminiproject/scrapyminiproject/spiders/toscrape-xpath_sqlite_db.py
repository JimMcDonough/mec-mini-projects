# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:46:44 2022

@author: jimmc
"""
import scrapy
import sqlite3
import json

def create_quotes_table(cursor, connection):
    sql = '''CREATE TABLE quotes (text_ text, author text, tags text)'''
    cursor.execute(sql)
    connection.commit()
    
def select_1_quote(cursor):
    sql = '''SELECT * FROM quotes limit 1'''
    return cursor.execute(sql).fetchall()

def insert_row(cursor,connection,text,author,tags):
    sql ="INSERT INTO quotes values (?,?,?)"
    cursor.execute(sql,(text,author,tags))
    connection.commit()


class QuotesSpider(scrapy.Spider):   
    name = "toscrape-xpath_db"
    
    start_urls = [
               'http://quotes.toscrape.com/page/1/',
           ]
    
    def parse(self, response):
        con = sqlite3.connect('quotes_DB.db')
        cur = con.cursor()
        
        try:
            select_1_quote(cur)
        except:
            create_quotes_table(cur, con)
            
        for quote in response.xpath("//div[@class = 'quote']"):
            
            insert_row(cur, con, quote.xpath(".//span[@class = 'text']/text()").get(), \
                       quote.xpath(".//span/small[@class = 'author']/text()").get(), \
                       json.dumps(quote.xpath(".//div[@class = 'tags']/a[@class = 'tag']/text()").getall()))    
            yield {
                'text': quote.xpath(".//span[@class = 'text']/text()").get(),
                'author': quote.xpath(".//span/small[@class = 'author']/text()").get(),
                'tags': quote.xpath(".//div[@class = 'tags']/a[@class = 'tag']/text()").getall(),
            }
        con.close()
        try:   
            next_page = response.xpath("//li[@class = 'next']/a").attrib['href']
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
        except:
           
            pass
            