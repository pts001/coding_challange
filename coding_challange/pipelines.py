import os
from scrapy.exporters import JsonLinesItemExporter


class SosItemExporter(object):
    def __init__(self):
        self.file = open("new_file.jsonl", 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()


    def close_spider(self, spider):
        self.exporter.finish_exporting()
        os.rename("new_file.jsonl", f"{spider.name}_output.jsonl")
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
