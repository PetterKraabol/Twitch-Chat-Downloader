#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

from app import Arguments, Settings, Downloader


def main() -> None:
    # Print version number
    if Arguments().version:
        print('Twitch Chat Downloader', Settings().config['version'])
        exit()

    # List formats
    if Arguments().formats:
        for format_name in [f for f in Settings().config['formats'] if f not in ['all']]:
            format_dictionary = Settings().config['formats'][format_name]
            if 'comments' in format_dictionary:
                print('\tcomment: {}'.format(Settings().config['formats'][format_name]['comments']['format']))
            if 'output' in format_dictionary:
                print('\toutput: {}'.format(Settings().config['formats'][format_name]['output']['format']))
            print('\n')

    # Download
    downloader = Downloader()
    if Arguments().video:
        downloader.videos([Arguments().video])
    elif Arguments().channel:
        downloader.channel(Arguments().channel)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitch Chat Downloader')
    parser.add_argument('-v', '--video', type=str, help='Video ID')
    parser.add_argument('-c', '--channel', type=str, help='Channel name')
    parser.add_argument('--limit', type=int, default=5, help='Number of videos from channel')
    parser.add_argument('--client_id', '--', type=str, help='Twitch client ID')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-o', '--output', type=str, help='Output folder', default='./output')
    parser.add_argument('-f', '--format', type=str, help='Message format', default='default')
    parser.add_argument('--start', type=int, help='Start time in seconds from video start')
    parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')
    parser.add_argument('--timezone', type=str, help='Timezone name')
    parser.add_argument('--init', action='store_true', help='Script setup')
    parser.add_argument('--update', action='store_true', help='Update settings')
    parser.add_argument('--version', action='store_true', help='Settings version')
    parser.add_argument('--formats', action='store_true', help='List available formats')
    parser.add_argument('--preview', action='store_true', help='Print chat lines')
    parser.add_argument('--input', type=str, help='Read data from JSON file')
    parser.add_argument('--settings', type=str, default=str(Path.home()) + '/.tcd/settings.json',
                        help='Custom settings file')

    Arguments(parser.parse_args().__dict__)
    Settings(Arguments().settings_file,
             reference_filepath=f'{os.path.dirname(os.path.abspath(__file__))}/settings.reference.json')
    main()
