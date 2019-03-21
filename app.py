#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

from app import Arguments, Settings, Downloader, Logger


def main():
    # Print version number
    if Arguments().print_version:
        Logger().log('Twitch Chat Downloader {}'.format(Settings().config['version']), retain=False)
        exit()

    # Update application
    if Arguments().update:
        Logger().log('Update: unimplemented', retain=False)
        exit()

    if Arguments().init:
        Logger().log('Init: unimplemented', retain=False)
        exit()

    # List formats
    if Arguments().print_formats:
        for format_name in [f for f in Settings().config['formats'] if f not in ['all']]:
            format_dictionary = Settings().config['formats'][format_name]
            Logger().log(f'[{format_name}]', retain=False)

            if 'comments' in format_dictionary:
                print('comment: {}'.format(Settings().config['formats'][format_name]['comments']['format']))

            if 'output' in format_dictionary:
                print('output: {}'.format(Settings().config['formats'][format_name]['output']['format']))

            Logger().log('\n', retain=False)
        exit()

    # Downloader
    downloader = Downloader()

    if Arguments().video_ids:
        downloader.videos(Arguments().video_ids)

    if Arguments().channels:
        downloader.channels(Arguments().channels)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitch Chat Downloader')
    parser.add_argument('-v', f'--{Arguments.Name.VIDEO}', type=str, help='Video IDs separated by commas')
    parser.add_argument('-c', f'--{Arguments.Name.CHANNEL}', type=str, help='Channel name')
    parser.add_argument(f'--{Arguments.Name.FIRST}', type=int, default=5, help='Use the first n videos from channel')
    parser.add_argument(f'--{Arguments.Name.CLIENT_ID}', type=str, help='Twitch client ID')
    parser.add_argument(f'--{Arguments.Name.VERBOSE}', action='store_true', help='Verbose output')
    parser.add_argument('-q', f'--{Arguments.Name.QUIET}', action='store_true')
    parser.add_argument('-o', f'--{Arguments.Name.OUTPUT}', type=str, help='Output folder', default='./output')
    parser.add_argument('-f', f'--{Arguments.Name.FORMAT}', type=str, help='Message format', default='default')
    parser.add_argument(f'--{Arguments.Name.START}', type=int, help='Start time in seconds from video start')
    parser.add_argument(f'--{Arguments.Name.STOP}', type=int, help='Stop time in seconds from video start')
    parser.add_argument(f'--{Arguments.Name.TIMEZONE}', type=str, help='Timezone name')
    parser.add_argument(f'--{Arguments.Name.INIT}', action='store_true', help='Script setup')
    parser.add_argument(f'--{Arguments.Name.UPDATE}', action='store_true', help='Update settings')
    parser.add_argument(f'--{Arguments.Name.VERSION}', action='store_true', help='Settings version')
    parser.add_argument(f'--{Arguments.Name.FORMATS}', action='store_true', help='List available formats')
    parser.add_argument(f'--{Arguments.Name.PREVIEW}', action='store_true', help='Print chat lines')
    parser.add_argument(f'--{Arguments.Name.INPUT}', type=str, help='Read data from JSON file')
    parser.add_argument(f'--{Arguments.Name.SETTINGS_FILE}', type=str, default=str(Path.home()) + '/.tcd/settings.json',
                        help='Custom settings file')
    parser.add_argument(f'--{Arguments.Name.DEBUG}', action='store_true', help='Print debug messages')

    Arguments(parser.parse_args().__dict__)
    Settings(Arguments().settings_file,
             reference_filepath=f'{os.path.dirname(os.path.abspath(__file__))}/settings.reference.json')

    main()
