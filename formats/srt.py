import app
import twitch
from formats import formatter
from typing import Tuple, Generator
from itertools import chain


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    output = formatter.format_output(app.settings['formats']['srt']['output'], video)

    return generator(subtitles(video.comments)), output


def subtitles(comments: Generator[dict, None, None]) -> Generator[str, None, None]:
    for comment in comments:
        yield app.settings['formats']['srt']['comments'].format(comment)


def generator(lines: Generator[str, None, None]) -> Generator[str, None, None]:
    for line in chain(prefix(), lines, suffix()):
        yield line


def prefix() -> Generator[str, None, None]:
    yield ''


def suffix() -> Generator[str, None, None]:
    yield ''
