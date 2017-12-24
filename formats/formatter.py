import app
from formats import timestamp, srt, ssa
import twitch
from typing import Tuple


class Error(Exception):
    pass


class FormatNameError(Error):

    def __init__(self, message):
        self.message = message


def comments(comment_format: dict, video: twitch.Video) -> str:
    for comment in video.comments:

        if 'timestamp' in comment_format:
            comment['created_at'] = timestamp.use(comment_format['timestamp'],
                                                  comment['created_at'])

        yield comment_format['format'].format(**comment)


def output(output_format: dict, video: twitch.Video) -> str:
    if 'timestamp' in output_format:
        video.metadata['created_at'] = timestamp.use(output_format['timestamp'], video.metadata['created_at'])

    return '{}/{}'.format(app.arguments.output.rstrip('/').rstrip('\\'),
                          output_format['format'].format(**video.metadata))


def custom_format(type_format: dict, video: twitch.Video) -> Tuple[str, str]:
    return comments(type_format['comments'], video), output(type_format['output'], video)


def use(format_name: str, video: twitch.Video) -> Tuple[str, str]:
    if format_name not in app.config.settings['formats']:
        raise FormatNameError('Unknown format: {}'.format(format_name))

    return {
        # 'srt': srt(video),
        # 'ssa': ssa(video)
    }.get(format_name, custom_format(app.config.settings['formats'][format_name], video))
