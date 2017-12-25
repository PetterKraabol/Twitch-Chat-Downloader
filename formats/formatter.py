import app
import twitch
from formats import timestamp, irc, srt, ssa
from typing import Tuple, Generator


class Error(Exception):
    pass


class FormatNameError(Error):

    def __init__(self, message):
        self.message = message


def use(format_name: str, video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    if format_name not in app.config.settings['formats']:
        raise FormatNameError('Unknown format: {}'.format(format_name))

    return {
        'srt': srt.use(video),
        'ssa': ssa.use(video),
        'irc': irc.use(video),
    }.get(format_name, custom_format(app.config.settings['formats'][format_name], video))


def custom_format(type_format: dict, video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    return format_comments(type_format['comments'], video.comments), format_output(type_format['output'], video)


def format_comments(comment_format: dict, comments: Generator[dict, None, None]) -> Generator[str, None, None]:
    for comment in comments:

        if 'timestamp' in comment_format:
            comment['created_at'] = timestamp.use(comment_format['timestamp'], comment['created_at'])

        yield format_comment(comment_format, comment)


def format_comment(comment_format: dict, comment: dict) -> str:
    return comment_format['format'].format(**comment)


def format_output(output_format: dict, video: twitch.Video) -> str:
    if 'timestamp' in output_format:
        video.metadata['created_at'] = timestamp.use(output_format['timestamp'], video.metadata['created_at'])

    return '{}/{}'.format(app.arguments.output.rstrip('/').rstrip('\\'),
                          output_format['format'].format(**video.metadata))
