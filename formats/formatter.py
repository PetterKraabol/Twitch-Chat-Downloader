import app.config
from formats import timestamp


class Error(Exception):
    pass


class FormatNameError(Error):

    def __init__(self, message):
        self.message = message


def custom_format(comment_format: str, comment: dict) -> str:
    return comment_format.format(**comment)


def use(format_name: str, comment: dict) -> str:
    if format_name not in app.config.settings['formats']:
        raise FormatNameError('Unknown format: {}'.format(format_name))

    # Format timestamp
    comment['created_at'] = timestamp.use(app.config.settings['formats'][format_name]['timestamp'],
                                          comment['created_at'])

    return custom_format(app.config.settings['formats'][format_name]['format'], comment)
