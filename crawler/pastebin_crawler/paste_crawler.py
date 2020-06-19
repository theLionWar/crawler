from typing import Dict, List

from lxml import html
import arrow
import requests
from requests.models import Response
from crawler.generic_crawler.crawler import Parser, CrawledItem
from crawler.pastebin_crawler.utils import parse_text_time_ago_to_mins


class Paste(CrawledItem):

    def __init__(self, author: str, title: str,
                 content: str, date: arrow.Arrow):
        self.author = author
        self.title = title
        self.content = content
        self.date = date

    def to_json(self) -> Dict:
        json_result = super().to_json()
        json_result['date'] = self.date.for_json()
        return json_result


class PasteParser(Parser):

    domain = 'https://pastebin.com/'
    archive_resource = 'archive'
    raw_content_resource = 'raw'

    @staticmethod
    def get_author_by_raw_item(raw_item: html.HtmlElement) -> str:
        return raw_item.xpath("//div[@class='paste_box_line2']")[0]. \
            getchildren()[1].text

    @staticmethod
    def get_title_by_raw_item(raw_item: html.HtmlElement) -> str:
        return raw_item.xpath("//div[@class='paste_box_line1']")[0]. \
            get('title')

    @staticmethod
    def get_date_by_raw_item(raw_item: html.HtmlElement) -> arrow.Arrow:
        raw_date = raw_item.xpath("//div[@class='paste_box_line2']")[0]. \
            getchildren()[4].text
        return arrow.get(raw_date, 'MMM Do, YYYY')

    def get_content_by_item_id(self, item_id):
        content_url = f'{self.domain}{self.raw_content_resource}/{item_id}'
        return requests.get(content_url).text

    def get_list_page(self) -> Response:
        return requests.get(f'{self.domain}{self.archive_resource}')

    def get_raw_item(self, item_id: str) -> html.HtmlElement:

        paste_page = requests.get(f'{self.domain}{item_id}')
        return html.fromstring(paste_page.content)

    def parse_item(self, item_id: str) -> Paste:

        raw_item = self.get_raw_item(item_id)

        author = self.get_author_by_raw_item(raw_item)
        title = self.get_title_by_raw_item(raw_item)
        content = self.get_content_by_item_id(item_id)
        date = self.get_date_by_raw_item(raw_item)

        return Paste(author, title, content, date)

    @staticmethod
    def get_raw_paste_table_by_raw_page(raw_page: html.HtmlElement) -> \
            html.HtmlElement:
        return raw_page.xpath("//table/tr")[1:]

    def is_newer_item(self, raw_paste: html.HtmlElement) -> bool:
        # newer pastes were posted not more than x minutes ago,
        # based on the interval

        interval_in_minutes = self.newer_interval_in_sec / 60

        posted_time_ago_str = raw_paste.getchildren()[1].text
        time_ago_in_mins = parse_text_time_ago_to_mins(posted_time_ago_str)
        if time_ago_in_mins < interval_in_minutes:
            return True

        return False

    @staticmethod
    def get_past_id_by_raw_paste(raw_paste: html.HtmlElement) -> str:
        return raw_paste.getchildren()[0].getchildren()[1].get('href')[1:]

    def get_newer_items_from_page(self, page: Response) -> List[str]:
        raw_page = html.fromstring(page.content)
        raw_paste_table = self.get_raw_paste_table_by_raw_page(raw_page)
        pastes_ids_list = []
        for raw_paste in raw_paste_table:
            if self.is_newer_item(raw_paste):
                pastes_ids_list.\
                    append(self.get_past_id_by_raw_paste(raw_paste))

        return pastes_ids_list
