from typing import Dict, List

import arrow
from lxml import html
import requests
from requests.models import Response

from crawler.generic_crawler.crawler import Parser, CrawledItem
from crawler.generic_crawler.exceptions import ParsingException, \
    ItemNotFoundException
from crawler.pastebin_crawler.data_noarmalization import PasteDataNormalizer
from crawler.pastebin_crawler.utils import parse_text_time_ago_to_mins


class Paste(CrawledItem):
    normalizer = PasteDataNormalizer()

    def __init__(self, author: str, title: str,
                 content: str, date: arrow.Arrow):
        self.author = self.normalizer.normalize_author(author)
        self.title = self.normalizer.normalize_title(title)
        self.content = self.normalizer.normalize_content(content)
        self.date = self.normalizer.normalize_date(date)

    def to_json(self) -> Dict:
        json_result = super().to_json()
        json_result['date'] = self.date.for_json()
        return json_result


class PasteParser(Parser):

    domain = 'https://pastebin.com/'
    archive_resource = 'archive'

    @staticmethod
    def get_author_by_raw_item(raw_item: html.HtmlElement) -> str:
        """
        parse the page to find and return author.
        :param raw_item: html element from Pastebin paste web page
        :return: the author of the Paste
        """
        try:
            return raw_item.xpath("//div[@class='paste_box_line2']")[0]. \
                getchildren()[1].text
        except IndexError as e:
            print(f'could not get author {e}')
            raise ItemNotFoundException from e

    @staticmethod
    def get_title_by_raw_item(raw_item: html.HtmlElement) -> str:
        """
        parse the page to find and return title.
        :param raw_item: html element from Pastebin paste web page
        :return: the title of the Paste
        """
        try:
            return raw_item.xpath("//div[@class='paste_box_line1']")[0]. \
                get('title')
        except IndexError as e:
            print(f'could not get title {e}')
            raise ItemNotFoundException from e

    @staticmethod
    def get_date_by_raw_item(raw_item: html.HtmlElement) -> arrow.Arrow:
        """
        parse the page to find and return date.
        :param raw_item: html element from Pastebin paste web page
        :return: the date of the Paste
        """
        try:
            potential_date_fields = raw_item. \
                xpath("//div[@class='paste_box_line2']")[0].getchildren()

            for potential_field in potential_date_fields:
                raw_date = potential_field.get('title')
                if raw_date:
                    # map unsupported timezone formats
                    raw_date = raw_date.replace('CDT', 'US/Central')
                    raw_date = raw_date.replace('EDT', 'US/Eastern')
                    raw_date = raw_date.replace('PST', 'US/Pacific')

                    return arrow.get(raw_date,
                                     'dddd Do of MMMM YYYY hh:mm:ss A ZZZ')

        except IndexError as e:
            print(f'could not get date {e}')
            raise ItemNotFoundException from e

        except arrow.ParserError as e:
            print(f'could not parse date {e}')
            raise ParsingException from e

    @staticmethod
    def get_content_by_raw_item(raw_item: html.HtmlElement):
        """
        parse the page to find and return content.
        :param raw_item: html element from Pastebin paste web page
        :return: the raw content of the Paste
        """
        try:
            return raw_item.xpath("//textarea[@id='paste_code']")[0].text
        except IndexError as e:
            print(f'could not get content {e}')
            raise ItemNotFoundException from e

    def get_list_page(self) -> Response:
        return requests.get(f'{self.domain}{self.archive_resource}')

    def get_raw_item(self, item_id: str) -> html.HtmlElement:
        paste_page = requests.get(f'{self.domain}{item_id}')
        return html.fromstring(paste_page.content)

    def parse_item(self, item_id: str) -> Paste:
        """
        :param item_id: paste hash id
        :return: Paste instance based on the given paste it
        """

        raw_item = self.get_raw_item(item_id)

        author = self.get_author_by_raw_item(raw_item)
        title = self.get_title_by_raw_item(raw_item)
        content = self.get_content_by_raw_item(raw_item)
        date = self.get_date_by_raw_item(raw_item)

        return Paste(author, title, content, date)

    @staticmethod
    def get_raw_paste_table_by_raw_page(raw_page: html.HtmlElement) -> \
            html.HtmlElement:
        return raw_page.xpath("//table/tr")[1:]

    def is_newer_item(self, raw_paste: html.HtmlElement) -> bool:
        """
        :param raw_paste: html element from Pastebin paste list web page
        :return: True if the paste was posted no more than x minutes ago,
        based on the crawling interval.
        """
        interval_in_mins = self.newer_interval_in_sec / 60

        posted_time_ago_str = raw_paste.getchildren()[1].text
        time_ago_in_mins = parse_text_time_ago_to_mins(posted_time_ago_str)
        if time_ago_in_mins < interval_in_mins:
            return True

        return False

    @staticmethod
    def get_past_id_by_raw_paste(raw_paste: html.HtmlElement) -> str:
        return raw_paste.getchildren()[0].getchildren()[1].get('href')[1:]

    def get_newer_items_from_page(self, page: Response) -> List[str]:
        # returns a list of Paste ids
        raw_page = html.fromstring(page.content)
        raw_paste_table = self.get_raw_paste_table_by_raw_page(raw_page)
        pastes_ids_list = []
        for raw_paste in raw_paste_table:
            if self.is_newer_item(raw_paste):
                pastes_ids_list.\
                    append(self.get_past_id_by_raw_paste(raw_paste))

        return pastes_ids_list
