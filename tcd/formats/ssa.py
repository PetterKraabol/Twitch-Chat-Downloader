import datetime
from itertools import chain
from typing import Tuple, Generator, List, Optional

from twitch.helix import Video
from twitch.v5 import Comment, Comments

from tcd.formats.format import Format
from tcd.pipe import Pipe
from tcd.safedict import SafeDict


class SSA(Format):
    OPEN: str = '[SSA_OPEN]'
    CLOSE: str = '[SSA_CLOSE]'
    SPECIAL: str = '♣'

    def __init__(self, video: Video):
        super().__init__(video, format_name='ssa')

    def use(self) -> Tuple[Generator[Tuple[str, Comment], None, None], str]:
        """
        Use SSA format
        :return:
        """
        output: str = Pipe(self.format_dictionary['output']).output(self.video.data)

        return self.generator(), output

    def generator(self) -> Generator[Tuple[str, Optional[Comment]], None, None]:
        """
        Line generator
        :return:
        """
        for line in chain(self.prefix(), self.dialogues(self.video.comments)):
            yield line

    @staticmethod
    def format_timestamp(time: datetime.timedelta) -> str:
        """
        Convert timedelta to h:mm:ss.cc
        https://www.matroska.org/technical/specs/subtitles/ssa.html

        :param time: Timedelta
        :return: Formatted time string
        """
        days, seconds = divmod(time.total_seconds(), 24 * 60 * 60)
        hours, seconds = divmod(seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)
        centiseconds = int((seconds - int(seconds)) * 100)

        # Floor seconds and merge days to hours
        seconds = int(seconds)
        hours += days * 24

        return f'{int(hours):01d}:{int(minutes):02d}:{int(seconds):02d}.{centiseconds:02d}'

    def dialogues(self, comments: Comments) -> Generator[Tuple[str, Comments], None, None]:
        """
        Format comments as SSA dialogues
        :param comments: Comment to format
        :return: tuple(formatted comment, comment)
        """
        for comment in comments:
            start: datetime.timedelta = datetime.timedelta(seconds=comment.content_offset_seconds)
            end: datetime.timedelta = start + datetime.timedelta(milliseconds=self.format_dictionary['duration'])

            # Avoid SSA variable conflicts with Python string formatting
            # This is done by temporarily removing opening and closing curly brackets used by SSA.
            #
            # The main problem is detecting these curly brackets. We want to differentiate brackets that
            # should be used by the Python string formatter, and those used by SSA.
            #
            # Opening curly brackets for SSA can easily be found by looking for "{\", however,
            # closing curly brackets are used in the same way (just a "}") for both and requires a bit more effort.
            #
            # By incrementing a counter for opening brackets meant for Python formatting and decrementing for every
            # closing bracket meant for Python formatting, we can define every closing bracket to belong to SSA whenever
            # the counter is at zero.

            ssa_closing_brackets_indices: list = []
            open_bracket_counter: int = 0

            # Loop through every character in formatting string
            for index in range(len(self.format_dictionary['comments']['format'])):
                letter: str = self.format_dictionary['comments']['format'][index]

                # Check if SSA bracket first, before altering the counter.
                if letter is '}' and open_bracket_counter is 0:
                    ssa_closing_brackets_indices.append(index)
                    continue

                # Update counter
                open_bracket_counter += {
                    '{': 1,  # Bracket is opened
                    '\\': -1,  # Bracket was meant for SSA, not for Python
                    '}': -1  # Closing bracket
                }.get(letter, 0)

                # Multiple SSA commands within a curly brackets could make it negative
                # Example: {\\c&#000000&\\b1} will count 1, 0, -1, -2
                open_bracket_counter = max(0, open_bracket_counter)

            # Add a temporary special character for SSA closing curly brackets
            for index in ssa_closing_brackets_indices:
                self.format_dictionary['comments']['format'] = self.format_dictionary['comments']['format'][
                                                               :index] + SSA.SPECIAL + \
                                                               self.format_dictionary['comments']['format'][index + 1:]

            self.format_dictionary['comments']['format'] = self.format_dictionary['comments']['format'].replace('{\\',
                                                                                                                SSA.OPEN).replace(
                SSA.SPECIAL, SSA.CLOSE)

            # Format comment
            comment_text = Pipe(self.format_dictionary['comments']).comment(comment.data)

            # Insert opening and closing curly brackets for SSA
            comment_text = comment_text.replace(SSA.OPEN, '{\\').replace(SSA.CLOSE, '}')

            # Convert color code into SSA color code.
            comment_text = comment_text.replace('\\c&#', '\\c&H').replace('\\c&H#', '\\c&H')

            dialogue: dict = {
                'start': SSA.format_timestamp(start),
                'end': SSA.format_timestamp(end),
                'comment': comment_text
            }
            dialogue.update(comment.data)

            yield self.format_dictionary['events']['dialogue'].format_map(SafeDict(dialogue)), comment

    def prefix(self) -> Generator[Tuple[str, None], None, None]:
        """
        SSA file header
        :return: Generator for header lines
        """
        lines: List[str] = list()

        # Script info
        lines.append('[Script Info]')
        lines.append('Title: {title}'.format_map(SafeDict(self.video.data)))
        lines.append('ScriptType: v4.00')
        lines.append('Collisions: Normal')
        lines.append('PlayResX: {resolution[x]}'.format_map(SafeDict(self.format_dictionary)))
        lines.append('PlayResY: {resolution[y]}'.format_map(SafeDict(self.format_dictionary)))
        lines.append('PlayDepth: 0')
        lines.append('Timer: 100,0000')

        # V4 Styles
        lines.append('\n[V4 Styles]')
        lines.append(self.format_dictionary['styles']['format'])
        lines.append(self.format_dictionary['styles']['values'])

        # Fonts
        lines.append('\n[Fonts]')
        lines.append(self.format_dictionary['fonts'])

        # Graphics
        lines.append('\n[Graphics]')
        lines.append(self.format_dictionary['graphics'])

        # Events
        lines.append('\n[Events]')
        lines.append(self.format_dictionary['events']['format'])

        for line in lines:
            yield line, None
