# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from itemadapter import ItemAdapter

class CSVWriterPipeline:
    def open_spider(self, spider):
        self.file = open('scraped_data.csv', 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=spider.field_names)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

