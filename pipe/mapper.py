import app
from pipe import timestamp


def use(dictionary: dict, format_dictionary: dict):
    """
    Map new values onto dictionary
    :param dictionary: input
    :param format_dictionary: input format dictionary
    :return nothing
    """

    # Timestamps
    if 'timestamp' in format_dictionary and '{timestamp' in format_dictionary['format']:

        dictionary['timestamp'] = {}

        # Absolute timestamp
        if 'absolute' in format_dictionary['timestamp'] and '{timestamp[absolute]}' in format_dictionary['format']:
            dictionary['timestamp']['absolute'] = timestamp.use(format_dictionary['timestamp']['absolute'],
                                                                dictionary['created_at'],
                                                                app.arguments.timezone)

        # Relative timestamp
        if '{timestamp[relative]}' in format_dictionary['format']:
            # Todo: 'relative' in format_dictionary['timestamp'] when relative formatting is implemented.
            dictionary['timestamp']['relative'] = timestamp.relative(float(dictionary['content_offset_seconds']))

    # IRC badge
    if 'commenter' in dictionary:
        if 'user_badges' not in dictionary['message']:
            dictionary['message']['user_badges'] = [{'_id': '', 'version': 1}]

        dictionary['commenter']['irc_badge'] = {
            'subscriber': '+',
            'moderator': '@',
            'global_mod': '%',
            'admin': '&',
            'staff': '!',
            'broadcaster': '~',
        }.get(dictionary['message']['user_badges'][0]['_id'], '')
