import dateutil.parser
from datetime import datetime


def parse_timestamp(value: str) -> datetime:
    return dateutil.parser.parse(value)


def use(date_format: str, date_value: str) -> str:
    return parse_timestamp(date_value).strftime(date_format)
