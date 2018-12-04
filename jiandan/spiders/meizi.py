# -*- coding: utf-8 -*-
import scrapy
from jiandan.items import MeiziItem
from selenium import webdriver

# browser = webdriver.Chrome()
# browser.maximize_window()
options = webdriver.ChromeOptions()  # 设置无界面模式，chrome59版本后
options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options)


class JiandanSpider(scrapy.Spider):
    name = 'jiandan'
    allowed_domains = ['jiandan.net']
    base_url = 'http://jandan.net/ooxx/page-{page}'

    def start_requests(self):
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            url = self.base_url.format(page=page)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        browser.get(response.url)
        browser.implicitly_wait(15)  # 设置隐性等待时间
        image_urls = browser.find_elements_by_link_text("[查看原图]")
        for image in image_urls:
            item = MeiziItem()
            item['img_url'] = image.get_attribute('href')
            yield item
