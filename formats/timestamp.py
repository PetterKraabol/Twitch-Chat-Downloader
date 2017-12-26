import twitch
import dateutil.parser
from datetime import datetime


def parse_timestamp(value: str) -> datetime:
    return dateutil.parser.parse(value)


def use(date_format: str, date_value: str) -> str:
    return parse_timestamp(date_value).strftime(date_format)


def relative(video: twitch.Video, comment: dict) -> int:
    start: datetime = parse_timestamp(video.metadata['created_at'])
    stop: datetime = parse_timestamp(comment['created_at'])

    return stop.time() - start.time()
