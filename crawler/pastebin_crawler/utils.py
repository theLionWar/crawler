
def parse_text_time_ago_to_mins(text_time_ago: str) -> float:

    if 'sec ago' in text_time_ago:
        return int(text_time_ago.replace(' sec ago', '')) / 60

    if 'min ago' in text_time_ago:
        return int(text_time_ago.replace(' min ago', ''))

    if 'hour ago' in text_time_ago:
        return int(text_time_ago.replace(' hour ago', '')) * 60

    if 'hours ago' in text_time_ago:
        return int(text_time_ago.replace(' hours ago', '')) * 60
