import app
import twitch
import datetime
from formats import formatter, timestamp
from typing import Tuple, Generator

FORMAT: dict = app.settings['formats']['srt']


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    output = formatter.format_output(FORMAT['output'], video)
    return subtitles(video), output


def subtitles(video: twitch.Video) -> Generator[str, None, None]:
    for index, comment in enumerate(video.comments):
        start: datetime.timedelta = datetime.timedelta(seconds=comment['content_offset_seconds'], milliseconds=0.001)
        stop: datetime.timedelta = start + datetime.timedelta(milliseconds=FORMAT['duration'])

        yield '{index}\n{start} --> {stop}\n{message}\n'.format(index=index + 1,
                                                                start=str(start).replace('.', ',')[:-3],
                                                                stop=str(stop).replace('.', ',')[:-3],
                                                                message=FORMAT['comments']['format'].format(**comment))
