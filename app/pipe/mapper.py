import hashlib
from typing import List

import app
from app.pipe import timestamp


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
    if 'message' in dictionary:

        # Set color
        if 'user_color' not in dictionary['message']:
            if 'default_user_color' in format_dictionary and format_dictionary['default_user_color'] not in ['random',
                                                                                                             'hash']:
                dictionary['message']['user_color'] = format_dictionary['default_user_color']
            else:
                # Assign color based on commenter's ID
                sha256 = hashlib.sha256()
                sha256.update(str.encode(dictionary['commenter']['_id']))

                # Truncate hash and mod it by 0xffffff-1 for color hex.
                color: str = hex(int(sha256.hexdigest()[:32], 16) % int(hex(0xffffff), 16)).lstrip('0x')

                # Add any missing digits
                while len(color) < 6:
                    color = color + '0'

                dictionary['message']['user_color'] = '#{color}'.format(color=color[:6])

        # SSA Color
        if 'message[ssa_user_color]' in format_dictionary['format']:
            dictionary['message']['ssa_user_color'] = '#{b}{g}{r}'.format(
                b=dictionary['message']['user_color'][5:7],
                g=dictionary['message']['user_color'][3:5],
                r=dictionary['message']['user_color'][1:3])

    # User badges
    # The Twitch API returns an array of badges, ordered by their importance (descending).
    if '{commenter[badge]}' in format_dictionary['format'] and 'message' in dictionary:

        # Add empty badge if no badge
        if 'user_badges' not in dictionary['message']:
            dictionary['message']['user_badges'] = [{'_id': '', 'version': 1}]

        # Default badges
        if 'badges' not in format_dictionary:
            format_dictionary['badges'] = {
                'turbo': '[turbo]',
                'premium': '[prime]',
                'bits': '[bits]',
                'subscriber': '[subscriber]',
                'moderator': '[moderator]',
                'global_mod': '[global mod]',
                'admin': '[admin]',
                'staff': '[staff]',
                'broadcaster': '[streamer]',
            }

        # Default badges setting
        if 'multiple_badges' not in format_dictionary:
            format_dictionary['multiple_badges'] = False

        # Get badge display text
        badges: List[str] = []
        for badge in dictionary['message']['user_badges']:
            badges.append(format_dictionary['badges'].get(badge['_id'], ''))

        # Display multiple badges or not
        if format_dictionary['multiple_badges']:
            dictionary['commenter']['badge'] = ''.join(badges)
        else:
            dictionary['commenter']['badge'] = ''

            # Find first defined user badge
            for badge in badges:
                if badge != '':
                    dictionary['commenter']['badge'] = badge
                    break
