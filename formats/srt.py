import app
import pipe
import twitch
import datetime
from typing import Tuple, Generator

irc_format: dict = app.settings['formats']['srt']


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    output = pipe.output(video.metadata, irc_format['output'])
    return subtitles(video.comments), output


def subtitles(comments: Generator[dict, None, None]) -> Generator[str, None, None]:
    for index, comment in enumerate(comments):
        start: datetime.timedelta = datetime.timedelta(seconds=comment['content_offset_seconds'], milliseconds=0.001)
        stop: datetime.timedelta = start + datetime.timedelta(milliseconds=irc_format['duration'])

        yield '{index}\n{start} --> {stop}\n{message}\n'.format(index=index + 1,
                                                                start=str(start).replace('.', ',')[:-3],
                                                                stop=str(stop).replace('.', ',')[:-3],
                                                                message=pipe.comment(comment, irc_format['comments']))
