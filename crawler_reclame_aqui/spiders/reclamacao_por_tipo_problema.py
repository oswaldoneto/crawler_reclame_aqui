import scrapy
import time
from selenium import webdriver

from crawler_reclame_aqui.items import ComplainItem


class QuoteSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self):
        chromedriver = "/usr/local/Cellar/chromedriver/2.29/bin/chromedriver"
        self.driver = webdriver.Chrome(chromedriver)  # Optional argument, if not specified will search path.

    def start_requests(self):
        urls = [
            'https://www.reclameaqui.com.br/indices/2708/unip - universidade - paulista/'
        ]
        for url in urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        self.driver.get(response.url)

        for a in self.driver.find_elements_by_xpath('//ul[@ng-if="business.topProblems.length > 0"]//li//span//a '):
            problem_type_url = a.get_attribute('href')
            yield scrapy.Request(url=problem_type_url, callback=self.parse_problem_type)

        #self.driver.quit()

    def parse_problem_type(self, response):

        self.driver.get(response.url)

        for a in self.driver.find_elements_by_xpath(
                '//div[@class="complaints-list"]//div[@class="complaint-item ng-scope"]//div[@class="complain-status-title"]//a'):
            complain_url = a.get_attribute('href')
            yield scrapy.Request(url=complain_url,
                                 callback=self.parse_complain)

    def parse_complain(self, response):

        self.driver.get(response.url)

        title = self.driver.find_elements_by_xpath('//div[@class="complain-head"]//h1')[0].text
        description = self.driver.find_elements_by_xpath('//div[@class="complain-body"]//p')[0].text
        problem_type =  self.driver.find_elements_by_xpath('//ul[@class="tags list-inline"]//li[1]//a')[0].text

        c = ComplainItem()
        c['title'] = title
        c['complain'] = description
        c['category'] = problem_type

        yield c
