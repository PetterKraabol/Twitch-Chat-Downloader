import hashlib
import string
from datetime import datetime, timedelta
from typing import List, Optional

import dateutil.parser
from pytz import timezone

from .arguments import Arguments
from .safedict import SafeDict


class Pipe:
    """
    Pipe takes care of adding custom data fields and finally
    format data into comment and output file strings
    """

    def __init__(self, format_dictionary: dict):
        """
        Pipe
        :param format_dictionary: Comment format
        """
        self.format_dictionary: dict = format_dictionary
        self.valid_directory_characters: str = f'-_.() {string.ascii_letters}{string.digits}'

        # Combine regular format and action_format if provided.
        self.combined_formats: str = ''
        if 'format' in self.format_dictionary:
            self.combined_formats += self.format_dictionary['format']
        if 'action_format' in self.format_dictionary:
            self.combined_formats += self.format_dictionary['action_format']

    def format(self, data: dict) -> str:
        """
        Format comment
        :param data: Input data
        :return:
        """
        self.mapper(data)

        return self.reduce(data)

    def comment(self, comment_data: dict) -> str:
        """
        Format comment data to string
        :param comment_data: Comment data
        :return: Formatted comment line
        """
        return self.format(comment_data)

    def output(self, video_data: dict) -> str:
        """
        Format output path from data
        :param video_data: Video data
        :return: Output string
        """
        output_string = ''.join(c for c in self.format(video_data) if c in self.valid_directory_characters)
        return '{}/{}'.format(Arguments().output.rstrip('/').rstrip('\\'), output_string)

    @staticmethod
    def timestamp(date_format: str, date_value: str, timezone_name: Optional[str] = None) -> str:
        """
        Parse timestamp, format it and change timezone if a timezone name is given
        :param date_format: Wanted date format
        :param date_value: Input value to be parsed
        :param timezone_name: Timezone name
        :return: Timestamp in string format
        """
        date: datetime = dateutil.parser.parse(date_value)

        # Convert to another timezone
        if timezone_name is not None:
            date = date.astimezone(timezone(timezone_name))

        return date.strftime(date_format)

    @staticmethod
    def timestamp_relative(seconds: float) -> str:
        # Todo: support formatting
        delta = timedelta(seconds=seconds)
        delta = delta - timedelta(microseconds=delta.microseconds)
        return str(delta)

    def reduce(self, data: dict) -> str:
        """
        Main formatting

        Map data dictionary to format string
        :param data: Input data
        :return: Formatted string
        """

        # If action format is defined and comment is an action
        if 'action_format' in self.format_dictionary and 'is_action' in data and bool(data['is_action']):
            try:
                return str(self.format_dictionary['action_format']).format_map(SafeDict(data))
            except TypeError:
                print('Invalid action format in settings file:', self.format_dictionary['is_action'])
                exit(1)
        else:
            try:
                return str(self.format_dictionary['format']).format_map(SafeDict(data))
            except TypeError:
                print('Invalid format in settings file:', self.format_dictionary['format'])
                exit(1)

    def mapper(self, data: dict) -> dict:
        """
        Make custom changes to the input data according to the format dictionary
        :param data: Input data
        :return: Data (input data dict is mutated)
        """

        # Timestamps
        if 'timestamp' in self.format_dictionary and '{timestamp' in self.combined_formats:

            data['timestamp'] = {}

            # Absolute timestamp
            if 'absolute' in self.format_dictionary['timestamp'] and '{timestamp[absolute]}' in self.combined_formats:

                # Millisecond precision - remove $f (milliseconds) from time format
                if 'millisecond_precision' in self.format_dictionary:
                    self.format_dictionary['timestamp']['absolute'] = str(
                        self.format_dictionary['timestamp']['absolute']).replace(
                        '%f', '_MILLISECONDS_')

                # Format timestamp
                data['timestamp']['absolute'] = self.timestamp(self.format_dictionary['timestamp']['absolute'],
                                                               data['created_at'],
                                                               Arguments().timezone)

                # Millisecond precision - add milliseconds to timestamp
                if 'millisecond_precision' in self.format_dictionary:
                    milliseconds: str = self.timestamp('%f', data['created_at'], Arguments().timezone)
                    milliseconds = milliseconds[:self.format_dictionary['millisecond_precision']]
                    data['timestamp']['absolute'] = str(data['timestamp']['absolute']).replace(
                        '_MILLISECONDS_',
                        milliseconds)

            # Relative timestamp
            if '{timestamp[relative]}' in self.combined_formats:
                # Todo: 'relative' in self.format_dictionary['timestamp'] when relative formatting is implemented.
                data['timestamp']['relative'] = self.timestamp_relative(
                    float(data['content_offset_seconds']))

        # User colors
        if 'message' in data:

            # Set color
            if 'user_color' not in data['message']:
                if 'default_user_color' in self.format_dictionary and self.format_dictionary[
                    'default_user_color'] not in ['random',
                                                  'hash']:
                    data['message']['user_color'] = self.format_dictionary['default_user_color']
                else:
                    # Assign color based on commenter's ID
                    sha256 = hashlib.sha256()
                    sha256.update(str.encode(data['commenter']['_id']))

                    # Truncate hash and mod it by 0xffffff-1 for color hex.
                    color: str = hex(int(sha256.hexdigest()[:32], 16) % int(hex(0xffffff), 16)).lstrip('0x')

                    # Add any missing digits
                    while len(color) < 6:
                        color = color + '0'

                    data['message']['user_color'] = '#{color}'.format(color=color[:6])

            # SSA Color
            if 'message[ssa_user_color]' in self.combined_formats:
                data['message']['ssa_user_color'] = '#{b}{g}{r}'.format(
                    b=data['message']['user_color'][5:7],
                    g=data['message']['user_color'][3:5],
                    r=data['message']['user_color'][1:3])

        # User badges
        # The Twitch API returns an array of badges, ordered by their importance (descending).
        if '{commenter[badge]}' in self.combined_formats and 'message' in data:

            # Add empty badge if no badge
            if 'user_badges' not in data['message']:
                data['message']['user_badges'] = [{'_id': '', 'version': 1}]

            # Default badges
            if 'badges' not in self.format_dictionary:
                self.format_dictionary['badges'] = {
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
            if 'multiple_badges' not in self.format_dictionary:
                self.format_dictionary['multiple_badges'] = False

            # Get badge display text
            badges: List[str] = []
            for badge in data['message']['user_badges']:
                badges.append(self.format_dictionary['badges'].get(badge['_id'], ''))

            # Display multiple badges or not
            if self.format_dictionary['multiple_badges']:
                data['commenter']['badge'] = ''.join(badges)
            else:
                data['commenter']['badge'] = ''

                # Find first defined user badge
                for badge in badges:
                    if badge != '':
                        data['commenter']['badge'] = badge
                        break

        return data
