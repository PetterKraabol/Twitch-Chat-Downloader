import app
import twitch
from pipe import timestamp
from typing import Tuple, Generator, Union
from formats import custom, srt, ssa, json as _json


class Error(Exception):
    pass


class FormatNameError(Error):

    def __init__(self, message):
        self.message = message


def use(format_name: str, video: twitch.Video) -> Tuple[Generator[Union[str, dict], None, None], str]:

    # Check if format name exists
    if format_name not in app.config.settings['formats']:
        raise FormatNameError('Unknown format: {}'.format(format_name))

    # Select format method
    if format_name == 'json':
        return _json.use(video)
    if format_name == 'srt':
        return srt.use(video)
    if format_name == 'ssa':
        return ssa.use(video)
    else:
        return custom.use(app.config.settings['formats'][format_name], video)
