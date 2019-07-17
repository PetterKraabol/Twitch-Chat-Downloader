import datetime
from typing import Tuple, Generator

from twitch.helix import Video
from twitch.v5 import Comment, Comments

from tcd.formats.format import Format
from tcd.pipe import Pipe
from tcd.safedict import SafeDict


class SRT(Format):

    def __init__(self, video: Video):
        """
        Initialize SRT format
        :param video: Video object
        """
        super().__init__(video, format_name='srt')

    def use(self) -> Tuple[Generator[Tuple[str, Comment], None, None], str]:
        """
        Use SRT format
        :return: Comment generator and output string
        """
        return self.subtitles(self.video.comments), Pipe(self.format_dictionary['output']).output(self.video.data)

    @staticmethod
    def format_timestamp(time: datetime.timedelta) -> str:
        """
        Convert timedelta to hh:mm:ss.mmm
        https://matroska.org/technical/specs/subtitles/srt.html

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

        return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}'

    def subtitles(self, comments: Comments) -> Generator[Tuple[str, Comment], None, None]:
        """
        Subtitle generator
        :param comments: Comments to turn into subtitles
        :return: Generator with subtitles and subtitle data
        """
        for index, comment in enumerate(comments):
            # Stat and stop timestamps. Add a millisecond for timedelta to include millisecond digits
            start = datetime.timedelta(seconds=comment.content_offset_seconds)
            stop: datetime.timedelta = start + datetime.timedelta(milliseconds=self.format_dictionary['duration'])

            # Format message
            message: str = Pipe(self.format_dictionary['comments']).comment(comment.data)

            # Subtitle variables
            # Subtract the last three milliseconds form timestamp (required by SRT)
            subtitle: dict = {
                'index': index + 1,
                'start': SRT.format_timestamp(start),
                'stop': SRT.format_timestamp(stop),
                'message': message
            }

            yield '{index}\n{start} --> {stop}\n{message}\n'.format_map(SafeDict(subtitle)), comment
