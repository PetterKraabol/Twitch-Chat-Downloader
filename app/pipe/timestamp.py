from datetime import datetime, timedelta

import dateutil.parser
from pytz import timezone


def parse_timestamp(value: str) -> datetime:
    return dateutil.parser.parse(value)


def use(date_format: str, date_value: str, timezone_name: str = None) -> str:
    date: datetime = parse_timestamp(date_value)

    # Convert to another timezone
    if timezone_name is not None:
        date = date.astimezone(timezone(timezone_name))

    return date.strftime(date_format)


def relative(seconds: float) -> str:
    # Todo: support formatting
    delta = timedelta(seconds=seconds)
    delta = delta - timedelta(microseconds=delta.microseconds)
    return str(delta)
