from abc import ABC, abstractmethod
from typing import Dict
from requests.models import Response

from crawler.generic_crawler.exceptions import ParsingException
from crawler.storage_management.storages import StorageManager


class CrawledItem:

    def to_json(self) -> Dict:
        return self.__dict__


class Parser(ABC):

    def __init__(self, newer_interval_in_sec: int):
        self.newer_interval_in_sec = newer_interval_in_sec

    @abstractmethod
    def get_list_page(self) -> Response:
        pass

    @abstractmethod
    def parse_item(self, item_id: str) -> CrawledItem:
        pass

    @abstractmethod
    def get_newer_items_from_page(self, page: Response):
        pass


class Crawler:
    def __init__(self, parser: Parser, storage_manager: StorageManager):
        self.parser = parser
        self.storage_manager = storage_manager

    def store_latest_items(self):

        list_page = self.parser.get_list_page()
        item_ids = self.parser.get_newer_items_from_page(list_page)

        for item_id in item_ids:
            try:
                parsed_item = self.parser.parse_item(item_id)
                self.storage_manager.create(parsed_item.to_json())
                print(f'Successfully stored item: {item_id}')
            except ParsingException:
                print(f'Parsing Exception, Could not store item: {item_id}')

        print(f'Stored {len(item_ids)} new items')
