
class ParsingException(Exception):
    message = 'Could not parse item'


class ItemNotFoundException(Exception):
    message = 'Item not found'
