import csv
from collections import Counter
from datetime import datetime
from pep_parse.constants import BASE_DIR, TIME_FORMAT, CSV_HEADERS, UTF


class PepParsePipeline:
    def __init__(self):
        self.status_count = Counter()
        self.result_dir = BASE_DIR

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        filename = f'''{self.result_dir}/status_summary_{
            datetime.now().strftime(TIME_FORMAT)
            }.csv'''
        with open(filename, mode='w', encoding=UTF) as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
            for status, count in self.status_count.items():
                writer.writerow([status, count])
            writer.writerow(['Total', sum(self.status_count.values())])
