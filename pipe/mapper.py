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

            # Millisecond precision - remove $f (milliseconds) from time format
            if 'millisecond_precision' in format_dictionary:
                format_dictionary['timestamp']['absolute'] = str(format_dictionary['timestamp']['absolute']).replace(
                    '%f', '_MILLISECONDS_')

            # Format timestamp
            dictionary['timestamp']['absolute'] = timestamp.use(format_dictionary['timestamp']['absolute'],
                                                                dictionary['created_at'],
                                                                app.arguments.timezone)

            # Millisecond precision - add milliseconds to timestamp
            if 'millisecond_precision' in format_dictionary:
                milliseconds: str = timestamp.use('%f', dictionary['created_at'], app.arguments.timezone)
                milliseconds = milliseconds[:format_dictionary['millisecond_precision']]
                dictionary['timestamp']['absolute'] = str(dictionary['timestamp']['absolute']).replace('_MILLISECONDS_',
                                                                                                       milliseconds)

        # Relative timestamp
        if '{timestamp[relative]}' in format_dictionary['format']:
            # Todo: 'relative' in format_dictionary['timestamp'] when relative formatting is implemented.
            dictionary['timestamp']['relative'] = timestamp.relative(float(dictionary['content_offset_seconds']))

    # IRC badge
    if '{commenter[irc_badge]}' in format_dictionary['format'] and 'message' in dictionary:

        # Add empty badge if no badge
        if 'user_badges' not in dictionary['message']:
            dictionary['message']['user_badges'] = [{'_id': '', 'version': 1}]

        # Set irc badge to first (highest) badge.
        # The Twitch API returns an array of badges, where the most important is first.
        dictionary['commenter']['irc_badge'] = {
            'subscriber': '+',
            'moderator': '@',
            'global_mod': '%',
            'admin': '&',
            'staff': '§',
            'broadcaster': '~',
        }.get(dictionary['message']['user_badges'][0]['_id'], '')
