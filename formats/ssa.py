import app
import pipe
import twitch
import datetime
from itertools import chain
from typing import Tuple, Generator, List

ssa_format: dict = app.settings['formats']['ssa']


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

        text, comment_dictionary = pipe.comment(comment, ssa_format['comments'])

        dialogue: dict = {
            'start': str(start)[:-4],
            'end': str(end)[:-4],
            'name': comment['commenter']['display_name'],
            'text': text
        }

        yield ssa_format['events']['dialogue'].format(**dialogue), comment_dictionary


def prefix(video_metadata: dict) -> Generator[Tuple[str, dict], None, None]:
    lines: List[str] = list()

    # Script info
    lines.append('[Script Info]')
    lines.append('Title: {title}'.format(**video_metadata))
    lines.append('ScriptType: v4.00')
    lines.append('Collisions: Normal')
    lines.append('PlayResY: 1024')
    lines.append('PlayDepth: 0')
    lines.append('Timer: 100,0000')

    # V4 Styles
    lines.append('\n[V4 Styles]')
    lines.append(ssa_format['styles']['format'])
    lines.append(ssa_format['styles']['values'])

    # Events
    lines.append('\n[Events]')
    lines.append(ssa_format['events']['format'])

    for line in lines:
        yield line, {}
