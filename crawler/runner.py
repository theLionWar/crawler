import time

from crawler.generic_crawler.constants import DEFAULT_SCHEDULER_INTERVAL_SECS
from crawler.generic_crawler.crawler import Crawler
from crawler.pastebin_crawler.paste_crawler import PasteParser
from crawler.storage_management.storages import TinydbStorageManager


class Scheduler:

    def __init__(self, interval_in_sec=DEFAULT_SCHEDULER_INTERVAL_SECS):
        self.interval_in_sec = interval_in_sec

    def get_crawler(self) -> Crawler:
        """
        :return: Crawler instance, with Pastebin Parser
        and TinyDB storage manager.
        """
        parser = PasteParser(newer_interval_in_sec=self.interval_in_sec)
        storage = TinydbStorageManager(db_name='data/pastes.json')
        return Crawler(parser=parser, storage_manager=storage)

    def run(self):
        iterations_counter = 0
        initial_run = True

        crawler = self.get_crawler()

        print(f'Starting to crawl {crawler.parser.domain}')
        while True:
            iterations_counter += 1

            print(f'Starting crawling iteration {iterations_counter}')
            crawler.store_latest_items(initial_run)
            initial_run = False
            print(f'Finished crawling iteration {iterations_counter}')

            time.sleep(self.interval_in_sec)


Scheduler().run()
