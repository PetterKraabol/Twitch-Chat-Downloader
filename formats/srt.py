import app
import pipe
import twitch
import datetime
from typing import Tuple, Generator

irc_format: dict = app.settings['formats']['srt']


def use(video: twitch.Video) -> Tuple[Generator[Tuple[str, dict], None, None], str]:
    output = pipe.output(video.metadata, irc_format['output'])
    return subtitles(video.comments), output


def subtitles(comments: Generator[dict, None, None]) -> Generator[Tuple[str, dict], None, None]:
    for index, comment in enumerate(comments):
        start: datetime.timedelta = datetime.timedelta(seconds=comment['content_offset_seconds'], milliseconds=0.001)
        stop: datetime.timedelta = start + datetime.timedelta(milliseconds=irc_format['duration'])

        text, comment_dictionary = pipe.comment(comment, irc_format['comments'])

        subtitle: dict = {
            'index': int(index) + 1,
            'start': str(start).replace('.', ',')[:-3],
            'stop': str(stop).replace('.', ',')[:-3],
            'text': text
        }

        yield '{index}\n{start} --> {stop}\n{text}\n'.format(**subtitle), comment_dictionary
