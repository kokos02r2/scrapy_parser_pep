import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:
    def __init__(self):
        self.status_count = Counter()
        self.result_dir = BASE_DIR / 'results'

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        return item

    def close_spider(self, spider):
        filename = f'''{self.result_dir}/status_summary_{
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            }.csv'''
        with open(filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in self.status_count.items():
                writer.writerow([status, count])
            writer.writerow(['Total', sum(self.status_count.values())])
