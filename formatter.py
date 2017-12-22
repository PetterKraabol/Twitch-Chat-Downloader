import config


class Error(Exception):
    pass


class FormatNameError(Error):

    def __init__(self, message):
        self.message = message


def custom_format(comment_format: str, comment: dict) -> str:
    return comment_format.format(**comment)


def use(format_name: str, comment: dict) -> str:
    if format_name in config.settings['formats']:
        return custom_format(config.settings['formats'][format_name], comment)
    else:
        raise FormatNameError('Unknown format: {}'.format(format_name))
