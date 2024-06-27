# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime

suffix_output = "w7_example.json"

class PttPipeline:
    def open_spider(self, spider):
        currentDT = datetime.datetime.now()
        dictfilename = currentDT.strftime("%Y%m%d%H_") + suffix_output
        print(dictfilename)
        self.file = open(dictfilename, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        #in windows issue
        #self.file.write(line.encode('utf-8'))
        self.file.write(line)

        return item
