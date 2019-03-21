import datetime
from typing import Tuple, Generator

import twitch

from app.formats.format import Format
from app.pipe import Pipe
from app.safedict import SafeDict


class SRT(Format):

    def __init__(self, video: twitch.helix.Video):
        """
        Initialize SRT format
        :param video: Video object
        """
        super().__init__(video, format_name='srt')

    def use(self) -> Tuple[Generator[Tuple[str, twitch.v5.Comment], None, None], str]:
        """
        Use SRT format
        :return: Comment generator and output string
        """
        return self.subtitles(self.video.comments()), Pipe(self.format_dictionary['output']).output(self.video.data)

    def format_timestamp(self, time: datetime.timedelta) -> str:
        """
        Convert timedelta to h:mm:ss.cc
        https://www.matroska.org/technical/specs/subtitles/ssa.html

        :param time: Timedelta
        :return: Formatted time string
        """
        days, seconds = divmod(time.total_seconds(), 24 * 60 * 60)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)

        # Floor seconds and merge days to hours
        seconds = int(seconds)
        hours += days * 24

        return f'{int(hours):01d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}'

    def subtitles(self, comments: twitch.v5.Comments) -> Generator[Tuple[str, twitch.v5.Comment], None, None]:
        """
        Subtitle generator
        :param comments: Comments to turn into subtitles
        :return: Generator with subtitles and subtitle data
        """
        for index, comment in enumerate(comments):
            # Stat and stop timestamps. Add a millisecond for timedelta to include millisecond digits
            start = datetime.timedelta(seconds=comment.content_offset_seconds, milliseconds=0.001)
            stop: datetime.timedelta = start + datetime.timedelta(milliseconds=self.format_dictionary['duration'])

            # Format message
            message: str = Pipe(self.format_dictionary['comments']).comment(comment.data)

            # Subtitle variables
            # Subtract the last three milliseconds form timestamp (required by SRT)
            subtitle: dict = {
                'index': index + 1,
                'start': str(start).replace('.', ',')[:-3],
                'stop': str(stop).replace('.', ',')[:-3],
                'message': message
            }

            yield '{index}\n{start} --> {stop}\n{message}\n'.format_map(SafeDict(subtitle)), comment
