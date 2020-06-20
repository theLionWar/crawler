from abc import ABC, abstractmethod
from typing import Dict, List

from requests.models import Response

from crawler.generic_crawler.exceptions import ParsingException, \
    ItemNotFoundException
from crawler.storage_management.storages import StorageManager


class CrawledItem:

    def to_json(self) -> Dict:
        return self.__dict__


class Parser(ABC):

    def __init__(self, newer_interval_in_sec: int):
        self.newer_interval_in_sec = newer_interval_in_sec

    @abstractmethod
    def get_list_page(self) -> Response:
        """
        :return: Http response that contains the page
        with the list of items to parse
        """
        pass

    @abstractmethod
    def parse_item(self, item_id: str) -> CrawledItem:
        """
        :param item_id: The id of the item to parse
        :return: A parsed CrawledItem
        """
        pass

    @abstractmethod
    def get_newer_items_from_page(self, page: Response,
                                  initial_run: bool = False) -> List[str]:
        """
        :param page: Http response that contains the page
        with the list of items to parse
        :param initial_run: if its an initial run
        :return: a list of the newer item ids
        """
        pass


class Crawler:
    def __init__(self, parser: Parser, storage_manager: StorageManager):
        self.parser = parser
        self.storage_manager = storage_manager

    def store_latest_items(self, initial_run: bool = False):
        """
        Get latest items from website, parse, and store them
        """

        list_page = self.parser.get_list_page()
        item_ids = self.parser.get_newer_items_from_page(list_page,
                                                         initial_run)

        for item_id in item_ids:
            try:
                parsed_item = self.parser.parse_item(item_id)
                self.storage_manager.create(parsed_item.to_json())
            except ParsingException as e:
                print(f'{str(e)}. Could not store item: {item_id}')
            except ItemNotFoundException as e:
                print(f'{str(e)}. Could not store item: {item_id}')
            except Exception:
                print(f'Unexpected error. Could not store item: {item_id}')
            else:
                print(f'Successfully stored item: {item_id}')

        print(f'Stored {len(item_ids)} new items')
