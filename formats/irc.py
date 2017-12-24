import app
import twitch
from formats import formatter
from typing import Tuple, Generator
from itertools import chain


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    comments, output = formatter.custom_format(app.config.settings['formats']['irc'], video)

    return generator(comments), output


def generator(lines: Generator[str, None, None]) -> Generator[str, None, None]:
    for line in chain(prefix(), lines, suffix()):
        yield line


def prefix() -> Generator[str, None, None]:
    yield ''


def suffix() -> Generator[str, None, None]:
    yield ''
