import datetime
import json
import os
import re
import sys
from typing import List

import twitch

from app.arguments import Arguments
from app.formatter import Formatter
from app.pipe import Pipe
from app.settings import Settings


class Downloader:

    def __init__(self):
        self.helix_api = twitch.Helix(client_id=Settings().config['client_id'], use_cache=True)

        self.formats: List[str] = []
        self.whitelist: List[str] = []
        self.blacklist: List[str] = []

        # Populate format list according to whitelist and blacklist
        if Arguments().format == 'all':
            if 'all' in Settings().config['formats']:
                self.blacklist = Settings().config['formats']['all']['whitelist'] or []
                self.whitelist = Settings().config['formats']['all']['blacklist'] or []

                for format_name in [f for f in Settings().config['formats'].keys() if f not in ['all']]:
                    if (self.whitelist and format_name not in self.whitelist) or (
                        self.blacklist and format_name in self.blacklist):
                        pass
                    else:
                        self.formats.append(format_name)
        else:
            self.formats.append(Arguments().format)

    def videos(self, video_ids: List[str]) -> None:
        for video in self.helix_api.videos(video_ids):

            # Parse video duration
            regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
            parts = regex.match(video.duration)
            parts = parts.groupdict()

            time_params = {}
            for name, param in parts.items():
                if param:
                    time_params[name] = int(param)

            video_duration = datetime.timedelta(**time_params)

            formatter = Formatter(video)

            # Special case for JSON
            if 'json' in self.formats:
                output: str = Pipe(Settings().config['formats']['json']['output']).output(video.data)
                os.makedirs(os.path.dirname(output), exist_ok=True)

                data: dict = {
                    'video': video.data,
                    'comments': []
                }

                for comment in video.comments():
                    data['comments'].append(comment.data)
                    self.draw_progress(current=comment.content_offset_seconds,
                                       end=video_duration.seconds,
                                       description='json')

                with open(output, 'w') as file:
                    json.dump(data, file, indent=4, sort_keys=True)

                print(f'[json] {output}')
                self.formats.remove('json')

            # For each format
            for format_name in self.formats:
                # Get formatted lines and output file
                comment_tuple, output = formatter.use(format_name)

                os.makedirs(os.path.dirname(output), exist_ok=True)
                with open(output, '+w') as file:
                    for line, comment in comment_tuple:
                        if comment:
                            self.draw_progress(current=comment.content_offset_seconds,
                                               end=video_duration.seconds,
                                               description=format_name)

                        file.write(f'{line}\n')

                print(f'[{format_name}] {output}')

    def channel(self, channel: str) -> None:
        """
        Download videos by channel name
        :param channel:
        :return:
        """
        self.videos([video.id for video in self.helix_api.user(channel).videos(limit=Arguments().limit)])

    @staticmethod
    def draw_progress(current: float, end: float, description: str = 'Downloading') -> None:
        sys.stdout.write('[{}] {}%\r'.format(description, '%.2f' % min(current * 10 / end * 10, 100.00)))
        sys.stdout.flush()
