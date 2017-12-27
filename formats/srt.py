import app
import pipe
import twitch
import datetime
from formats import formats
from typing import Tuple, Generator

irc_format: dict = app.settings['formats']['srt']


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    output = formats.format_output(irc_format['output'], video)
    return subtitles(video), output


def subtitles(video: twitch.Video) -> Generator[str, None, None]:
    for index, comment in enumerate(video.comments):
        start: datetime.timedelta = datetime.timedelta(seconds=comment['content_offset_seconds'], milliseconds=0.001)
        stop: datetime.timedelta = start + datetime.timedelta(milliseconds=irc_format['duration'])

        yield '{index}\n{start} --> {stop}\n{message}\n'.format(index=index + 1,
                                                                start=str(start).replace('.', ',')[:-3],
                                                                stop=str(stop).replace('.', ',')[:-3],
                                                                message=pipe.comment(comment, irc_format['comments']))
