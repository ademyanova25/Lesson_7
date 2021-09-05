import scrapy
from scrapy.http import HtmlResponse
from Leroy_Merlin.items import LeroyMerlinItem
from scrapy.loader import ItemLoader


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroy_merlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/mebel-dlya-kuhni/']

    def parse(self, response:HtmlResponse):
        url_goods = response.xpath('//a[@data-qa="product-name"]/@href').getall()
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in url_goods:
            yield response.follow(url, callback=self.parse_leroy)

    def parse_leroy(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyMerlinItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photo', '//uc-pdp-media-carousel/picture/img/@src')
        loader.add_xpath('characteristic', '//div[@class="def-list__group"]/dt/text()')
        loader.add_xpath('value_char', '//div[@class="def-list__group"]/dd/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        yield loader.load_item()




