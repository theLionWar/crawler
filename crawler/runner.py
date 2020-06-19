import time
from crawler.generic_crawler.constants import DEFAULT_SCHEDULER_INTERVAL_SECS
from crawler.generic_crawler.crawler import Crawler
from crawler.pastebin_crawler.paste_crawler import PasteParser
from crawler.storage_management.storages import TinydbStorageManager


class Scheduler:

    def __init__(self, interval_in_sec=DEFAULT_SCHEDULER_INTERVAL_SECS):
        self.interval_in_sec = interval_in_sec

    def run(self):
        iterations_counter = 0
        print(f'Starting to crawl {PasteParser.domain}')
        while True:
            parser = PasteParser(newer_interval_in_sec=self.interval_in_sec)
            storage = TinydbStorageManager(db_name='data/pastes.json')

            crawler = Crawler(parser=parser, storage_manager=storage)
            crawler.store_latest_items()

            iterations_counter += 1
            print(f'Finished crawling iteration {iterations_counter}')
            time.sleep(self.interval_in_sec)


Scheduler().run()
