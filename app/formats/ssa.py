import datetime
from itertools import chain
from typing import Tuple, Generator, List

import app
import app.pipe as pipe
import app.twitch as twitch
from app.utils import SafeDict

ssa_format: dict = app.settings['formats']['ssa']

SSA_OPEN: str = '[SSA_OPEN]'
SSA_CLOSE: str = '[SSA_CLOSE]'
SSA_SPECIAL: str = '♣'


def use(video: twitch.Video) -> Tuple[Generator[Tuple[str, dict], None, None], str]:
    output = pipe.output(video.metadata, ssa_format['output'])

    return generator(video), output


def generator(video: twitch.Video) -> Generator[Tuple[str, dict], None, None]:
    for line in chain(prefix(video.metadata), dialogues(video.comments)):
        yield line


def dialogues(comments: Generator[dict, None, None]) -> Generator[Tuple[str, dict], None, None]:
    for comment in comments:
        start: datetime.timedelta = datetime.timedelta(seconds=comment['content_offset_seconds'], milliseconds=0.001)
        end: datetime.timedelta = start + datetime.timedelta(milliseconds=ssa_format['duration'])

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
        for index in range(len(ssa_format['comments']['format'])):
            letter: str = ssa_format['comments']['format'][index]

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
            ssa_format['comments']['format'] = ssa_format['comments']['format'][:index] + SSA_SPECIAL + \
                                               ssa_format['comments']['format'][index + 1:]

        ssa_format['comments']['format'] = ssa_format['comments']['format'].replace('{\\', SSA_OPEN).replace(
            SSA_SPECIAL, SSA_CLOSE)

        # Format comment
        comment_text = pipe.comment(comment, ssa_format['comments'])

        # Insert opening and closing curly brackets for SSA
        comment_text = comment_text.replace(SSA_OPEN, '{\\').replace(SSA_CLOSE, '}')

        # Convert color code into SSA color code.
        comment_text = comment_text.replace('\\c&#', '\\c&H').replace('\\c&H#', '\\c&H')

        dialogue: dict = {
            'start': str(start)[:-4],
            'end': str(end)[:-4],
            'comment': comment_text
        }
        dialogue.update(comment)

        yield ssa_format['events']['dialogue'].format_map(SafeDict(dialogue)), comment


def prefix(video_metadata: dict) -> Generator[Tuple[str, dict], None, None]:
    lines: List[str] = list()

    # Script info
    lines.append('[Script Info]')
    lines.append('Title: {title}'.format_map(SafeDict(video_metadata)))
    lines.append('ScriptType: v4.00')
    lines.append('Collisions: Normal')
    lines.append('PlayResX: {resolution[x]}'.format_map(SafeDict(ssa_format)))
    lines.append('PlayResY: {resolution[y]}'.format_map(SafeDict(ssa_format)))
    lines.append('PlayDepth: 0')
    lines.append('Timer: 100,0000')

    # V4 Styles
    lines.append('\n[V4 Styles]')
    lines.append(ssa_format['styles']['format'])
    lines.append(ssa_format['styles']['values'])

    # Fonts
    lines.append('\n[Fonts]')
    lines.append(ssa_format['fonts'])

    # Graphics
    lines.append('\n[Graphics]')
    lines.append(ssa_format['fonts'])

    # Events
    lines.append('\n[Events]')
    lines.append(ssa_format['events']['format'])

    for line in lines:
        yield line, {}
