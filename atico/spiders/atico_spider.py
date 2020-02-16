# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from ..items import PropertyItem


class AticoSpiderSpider(scrapy.Spider):
    name = 'atico_spider'

    def __init__(self, page_url='', url_file=None, *args, **kwargs):
        pages = 5
        self.start_urls = ['https://www.atico.es/resultados-de-la-busqueda/page/{}/'.format(i + 1) for i in
                           range(pages)]

        if not page_url and url_file is None:
            TypeError('No page URL or URL file passed.')

        if url_file is not None:
            with open(url_file, 'r') as f:
                self.start_urls = f.readlines()
        if page_url:
            # Replaces the list of URLs if url_file is also provided
            self.start_urls = [page_url]

        super().__init__(*args, **kwargs)

    def start_requests(self):
        for page in self.start_urls:
            logging.info("Scraping page: {}".format(page))
            yield scrapy.Request(url=page, callback=self.crawl_page)

    def crawl_page(self, response):
        property_urls = response.css('.property-item a.hover-effect::attr(href)').getall()
        for property in property_urls:
            logging.info("Scraping property: {}".format(property))
            yield scrapy.Request(url=property, callback=self.crawl_property)

    def crawl_property(self, response):
        property = PropertyItem()

        # Resource
        property["resource_url"] = "https://www.atico.es/"
        property["resource_title"] = 'Atico'
        property["resource_country"] = 'ES'

        # Property
        property["active"] = 1
        property["url"] = response.url
        property["title"] = response.xpath('.//*[@class="table-cell"]/h1/text()').get()
        property["subtitle"] = response.xpath('.//*[@class="descrip-corta"]/text()').get()
        property["location"] = self.get_location(response)
        property["extra_location"] = ''
        property["body"] = ';'.join(response.xpath('.//*[@id="description"]/p//text()').extract())

        # Price
        property["current_price"] = response.xpath('.//*[@class="header-right"]/span/text()').get()[:-1]
        property["original_price"] = response.xpath('.//*[@class="header-right"]/span/text()').get()[:-1]
        property["price_m2"] = ''
        property["area_market_price"] = ''
        property["square_meters"] = response.xpath('.//*[@class="ico-detail"]/span/text()').get()[:-3]

        # Details
        property["area"] = ''
        property["tags"] = self.get_tags(response)
        property["bedrooms"] = response.xpath('.//*[@class="ico-txt"]//text()').extract()[1][:1]
        property["bathrooms"] = response.xpath('.//*[@class="ico-txt"]//text()').extract()[2][:1]
        property["last_update"] = ''
        property["certification_status"] = response.xpath('.//*[@class="txt-certif"]/text()').get()
        property["consumption"] = ''
        property["emissions"] = response.xpath('.//*[@class="txt-certif"]/text()').get()

        # Multimedia
        property["main_image_url"] = self.get_main_img_url(response)
        property["image_urls"] = self.get_img_urls(response)
        property["floor_plan"] = ''
        property["energy_certificate"] = ''
        property["video"] = ''

        # Agents
        property["seller_type"] = ''
        property["agent"] = "ATICO Especialistas en Aticos"
        property["ref_agent"] = "ATICO Especialistas en Aticos"
        property["source"] = "ATICO Especialistas en Aticos"
        property["ref_source"] = self.get_reference(response)
        property["phone_number"] = ''

        # Additional
        property["additional_url"] = ''
        property["published"] = ''
        property["scraped_ts"] = ''

        yield property

    def get_img_url_list(self, response):
        img_url_wraps = response.xpath('//*[@id="gallery"]//@style').extract()
        extract_url = lambda url_wrap: re.search('url\((.*?)\)', url_wrap).group(1)
        return list(map(extract_url, img_url_wraps))

    def get_main_img_url(self, response):
        return self.get_img_url_list(response)[0]

    def get_img_urls(self, response):
        return ';'.join(self.get_img_url_list(response)[1:])

    def get_tags(self, response):
        property_type = ' '.join(response.xpath('//*[@id="detail"]/div[2]/ul/li[8]//text()').extract())
        garaje = ' '.join(response.xpath('//*[@id="detail"]/div[2]/ul/li[7]//text()').extract())
        characteristics = response.xpath('//*[@id="features"]//text()').extract()
        characteristics = list(filter(lambda x: '\n' not in x, characteristics))[1:-1]

        return ';'.join([property_type, garaje] + characteristics)

    def get_location(self, response):
        ciudad = ' '.join(response.xpath('.//*[@class="detail-city"]//text()').extract())
        barrio = ' '.join(response.xpath('.//*[@class="detail-area"]//text()').extract())

        return ';'.join([ciudad, barrio])

    def get_reference(self, response):
        full_reference = response.xpath("//*[@class='referencia']/text()").get()
        extract_ref_number = lambda reference: re.search('Ref. (\d+)', reference).group(1)
        return extract_ref_number(full_reference)

