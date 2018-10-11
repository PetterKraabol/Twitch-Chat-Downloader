import datetime
from typing import Tuple, Generator

import app
import app.pipe as pipe
import app.twitch as twitch
from app.utils import SafeDict

irc_format: dict = app.settings['formats']['srt']


def use(video: twitch.Video) -> Tuple[Generator[Tuple[str, dict], None, None], str]:
    return subtitles(video.comments), pipe.output(video.metadata, irc_format['output'])


def subtitles(comments: Generator[dict, None, None]) -> Generator[Tuple[str, dict], None, None]:
    for index, comment in enumerate(comments):
        # Start and stop timestamps. Add a millisecond for timedelta to include millisecond digits.
        start: datetime.timedelta = datetime.timedelta(seconds=comment['content_offset_seconds'], milliseconds=0.001)
        stop: datetime.timedelta = start + datetime.timedelta(milliseconds=irc_format['duration'])

        # Format message
        message = pipe.comment(comment, irc_format['comments'])

        # Subtitle variables
        # Subtract the last three millisecond digits from timestamps, required by srt.
        subtitle: dict = {
            'index': index + 1,
            'start': str(start).replace('.', ',')[:-3],
            'stop': str(stop).replace('.', ',')[:-3],
            'message': message
        }

        yield '{index}\n{start} --> {stop}\n{message}\n'.format_map(SafeDict(subtitle)), comment
