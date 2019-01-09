import json
import os
import sys
from typing import List

import twitch

from app.arguments import Arguments
from app.formatter import Formatter
from app.settings import Settings


class Downloader:

    def __init__(self):
        self.helix_api = twitch.Helix(client_id=Settings().config['client_id'], use_cache=True)
        self.formats: List[str] = []
        self.whitelist: List[str] = []
        self.blacklist: List[str] = []

        if Arguments().format == 'all':
            if 'all' in Settings().config['formats']:
                self.blacklist = Settings().config['formats']['all']['whitelist'] or []
                self.whitelist = Settings().config['formats']['all']['blackilst'] or []

                self.formats = [format_name for format_name in dict(Settings().config['formats']).keys() if
                                (self.whitelist and format_name not in self.whitelist) or
                                (self.blacklist and format_name not in self.blacklist)]
        else:
            self.formats.append(Arguments().format)

    def download_videos(self, video_ids: List[str]) -> None:
        """
        Download videos by IDs to files
        :param video_ids: List of video IDs
        :return: None
        """
        for video in self.helix_api.videos(video_ids):
            for format_name in self.formats:
                lines, output = Formatter(video).use(format_name)

                # Save to file
                if not os.path.exists(os.path.dirname(output)):
                    os.makedirs(os.path.dirname(output))

                with open(output, 'w+') as file:

                    # Special case for JSON
                    # todo: probably won't work in this solution because we don't download JSON data first
                    #   (input not guaranteed)
                    if format_name == 'json':
                        for data in lines:
                            json.dump(data, file, indent=4, sort_keys=True)
                    else:
                        for comment_line in lines:
                            print(comment_line)
                            file.write('{}\n'.format(comment_line))

        print('Finished downloading', video_ids)

    def download_channel(self, channel: str) -> None:
        """
        Download videos by channel name
        :param channel:
        :return:
        """
        self.download_videos([video.id for video in self.helix_api.user(channel).videos(limit=Arguments().limit)])

    @staticmethod
    def draw_progress(current: float, end: float, description: str = 'Downloading') -> None:
        sys.stdout.write('[{}] {}%\r'.format(description, '%.2f' % min(current * 10 / end * 10, 100.00)))
        sys.stdout.flush()
