import time
from crawler.generic_crawler.constants import DEFAULT_SCHEDULER_INTERVAL
from crawler.generic_crawler.crawler import Crawler
from crawler.pastebin_crawler.paste_crawler import PasteParser
from crawler.storage_management.storages import TinydbStorageManager


class Scheduler:

    def __init__(self, interval_in_sec=DEFAULT_SCHEDULER_INTERVAL):
        self.interval_in_sec = interval_in_sec

    def run(self):
        while True:
            parser = PasteParser(newer_interval_in_sec=self.interval_in_sec)
            storage = TinydbStorageManager(db_name='data/pastes.json')

            crawler = Crawler(parser=parser, storage_manager=storage)
            crawler.store_latest_items()

            time.sleep(self.interval_in_sec)


Scheduler().run()
