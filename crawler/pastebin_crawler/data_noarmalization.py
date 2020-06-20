import arrow


class PasteDataNormalizer:

    @staticmethod
    def normalize_author(author: str):
        # unifying unknown author to an empty string
        # convert to all lowercase
        author = author.lower()
        if author in ['guest', 'anonymous', 'unknown', '']:
            return ''
        return author

    @staticmethod
    def normalize_title(title: str):
        # all titles that includes "untitled" will be normalized to "untitled"
        # the title is capitalized
        title = title.lower()
        if 'untitled' in title:
            title = 'untitled'
        return title.capitalize()

    @staticmethod
    def normalize_date(date: arrow.Arrow):
        # returning UTC date
        return date.to('UTC')

    @staticmethod
    def normalize_content(content):
        # removing trailing slashes
        return content.strip('/')
