from app.utils import SafeDict
from typing import Tuple


def use(dictionary: dict, format_dictionary: dict) -> Tuple[str, dict]:
    """
    The reducer's job is to format an input to an output based on a format dictionary.
    :param dictionary:
    :param format_dictionary:
    :return: formatted string
    """
    # Action format
    if 'action_format' in format_dictionary and 'is_action' in dictionary and bool(dictionary['is_action']):
        return format_dictionary['action_format'].format_map(SafeDict(dictionary)), dictionary

    return format_dictionary['format'].format_map(SafeDict(dictionary)), dictionary
