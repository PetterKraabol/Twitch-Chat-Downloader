from typing import Tuple, Generator, Union

import app
import app.twitch as twitch
from app.formats import custom, srt, ssa, json as _json


def use(format_name: str, video: twitch.Video) -> Tuple[Generator[Union[Tuple[str, dict], dict], None, None], str]:
    # Check if format name exists
    if format_name not in app.config.settings['formats']:
        print('Unknown format: {}'.format(format_name))
        exit()

    # Select format method
    if format_name == 'json':
        return _json.use(video)
    if format_name == 'srt':
        return srt.use(video)
    if format_name == 'ssa':
        return ssa.use(video)
    else:
        return custom.use(app.config.settings['formats'][format_name], video)
