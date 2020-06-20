import arrow


class PasteDataNormalizer:

    @staticmethod
    def normalize_author(author: str) -> str:
        """
        unifying unknown author to an empty string,
        convert to all lowercase
        :param author: author original name
        :return: normalized author name
        """
        author = author.lower()
        if author in ['guest', 'anonymous', 'unknown', '']:
            return ''
        return author

    @staticmethod
    def normalize_title(title: str) -> str:
        """
        all titles that includes "untitled" will be normalized to "untitled",
        the title is capitalized
        :param title: original title
        :return: normalized title
        """
        title = title.lower()
        if 'untitled' in title:
            title = 'untitled'
        return title.capitalize()

    @staticmethod
    def normalize_date(date: arrow.Arrow) -> arrow.Arrow:
        """
        converts date to UTC.
        :param date: original date in any time zone
        :return: normalized date to UTC
        """
        return date.to('UTC')

    @staticmethod
    def normalize_content(content: str) -> str:
        """
        removing trailing slashes
        :param content: original content
        :return: normalized content
        """
        return content.strip('/')
