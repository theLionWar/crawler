from tinydb import TinyDB
from crawler.generic_crawler.crawler import StorageManager, CrawledItem


class FileStorageManager(StorageManager):

    def store(self, item):
        print('storing in a file')


class TinydbStorageManager(StorageManager):

    def __init__(self, db_name: str = 'data/default.json'):
        self.db = TinyDB(db_name)

    def store(self, item: CrawledItem):
        self.db.insert(item.to_json())
