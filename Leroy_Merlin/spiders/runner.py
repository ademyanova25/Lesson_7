from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from Leroy_Merlin import settings
from Leroy_Merlin.spiders.leroy_merlin import LeroyMerlinSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(crawler_settings)
    process.crawl(LeroyMerlinSpider)

    process.start()
