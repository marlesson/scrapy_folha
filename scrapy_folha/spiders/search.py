# -*- coding: utf-8 -*-
import scrapy
from scrapy_folha.items import ScrapyFolhaItem

class SearchSpider(scrapy.Spider):
    name = 'search'
    allowed_domains = ['search.folha.uol.com.br', 
                        'www1.folha.uol.com.br']

    start_urls = ['http://search.folha.uol.com.br/?q=*']

    def parse(self, response):
      for li in response.css("ol.search-results-list li"):
        link = li.css("a ::attr(href)").extract_first()  

        yield response.follow(link, self.parse_article)

      next_page = response.css("div.pagination a::attr(href)").extract()[-2]
      if next_page is not None:
          yield response.follow(next_page, self.parse)

    def parse_article(self, response):
      link       = response.url
      title      = response.css("article h1 ::text").extract_first()
      text       = "".join(response.css("article div.content p ::text").extract())
      created_at = "".join(response.css("article time ::text").extract())

      article = ScrapyFolhaItem(title=title, created_at=created_at, text=text, link=link)
      yield article      
