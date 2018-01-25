import app
import hashlib
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

    # User colors
    if 'message' in dictionary and 'user_color' not in dictionary['message']:

        # Set color
        if 'default_user_color' in format_dictionary and format_dictionary['default_user_color'] not in ['random',
                                                                                                         'hash']:
            dictionary['message']['user_color'] = format_dictionary['default_user_color']
        else:
            # Assign color based on commenter's ID
            sha256 = hashlib.sha256()
            sha256.update(str.encode(dictionary['commenter']['_id']))

            # Truncate hash and mod it by 0xffffff-1 for color hex.
            color: str = hex(int(sha256.hexdigest()[:32], 16) % int(hex(0xfffffe), 16))
            dictionary['message']['user_color'] = '#{color}'.format(color=str(color).strip('0x'))

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
