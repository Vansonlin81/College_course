# -*- coding: utf-8 -*-
import scrapy
import time
from ptt.items import PttItem
import logging

class PttspiderSpider(scrapy.Spider):
    name = 'pttSpider'
    allowed_domains = ['ptt.cc']
    start_index = 38966
    temp_str = 'https://www.ptt.cc/bbs/Gossiping/index%d.html'
    start_urls = [temp_str % (start_index)]

    _retries = 0
    MAX_RETRY = 100000 # 18歲問題的最大重試次數

    _pages = 0
    MAX_PAGES = 5 #100 # 最大翻頁次數

    def parse(self, response):  # 這個函式包括18歲問題表單傳送、爬取每一頁的每個標題，並將各文章連結傳給parse_post函式
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:   # 判斷是否進入18歲問題頁面
            if self._retries < self.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield scrapy.FormRequest.from_response(response,
                                                formdata={'yes': 'yes'},
                                                callback=self.parse)  # 表單送出後，再次呼叫parse函式
            else:
                logging.warning('you cannot pass')

        else:   
            self._pages += 1
            target = response.css("div.r-ent")
            for tag in target:
                try:
                    item = PttItem()
                    item['title'] = tag.css("div.title a::text").get()
                    item['author'] = tag.css('div.author::text').get()
                    item['date'] = tag.css('div.date::text').get()
                    item['push'] = tag.css('span::text').get()
                    item['url'] = response.urljoin(tag.css('div.title a::attr(href)').get())

                    if item['url']:
                        yield scrapy.Request(item['url'], meta={'pass_item': item}, callback=self.parse_article) # 將每個內文的網址傳送給parse_post，進行內文等相關內容的爬取

                except IndexError:
                    pass
                continue


            if self._pages < self.MAX_PAGES: # 判斷是否等於最大翻頁次數
                lastpage = u'上頁'
                next_page = response.xpath(
                    '//div[@id="action-bar-container"]//a[contains(text(), "%s")]/@href' %(lastpage))
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('follow {}'.format(url))
                    yield scrapy.Request(url, self.parse)
                else:
                    logging.warning('no next page')
            else:
                logging.warning('max pages reached')

    def parse_article(self, response):
        item = response.meta['pass_item']
        target = response.xpath("//*[@id='main-content']/text()")
        #//*[@id="main-content"]/text()
        #print(target.get())
        #//*[@id="main-content"]/text()[3]
        item['content'] = ''
        for content in target:
            #print(content.get())
            str_content = content.get()
            if str_content:
                item['content'] += str_content

        yield item

