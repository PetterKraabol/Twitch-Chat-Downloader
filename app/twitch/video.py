import json
from pathlib import Path
from typing import List, Generator

import twitch
import twitch.helix as helix

import app.cli
import app.config
import app.twitch.api as api


class Video:

    def __init__(self, video_id: str = None):

        # Check if data should be loaded from an input file or form the Twitch API
        if app.cli.arguments.input:
            if Path(app.cli.arguments.input).is_file():
                with open(app.cli.arguments.input, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)

                    # Check if JSON format is valid
                    if 'video' not in json_data or 'comments' not in json_data:
                        print('Error: Invalid JSON file.')
                        exit(1)

                    # Set metadata and comments
                    self.metadata = json_data['video']
                    self.comments = Video.comment_generator(json_data['comments'])

                    if app.cli.arguments.verbose:
                        print('Loaded json data form input file')
            else:
                print('Error: Unable to find {}'.format(app.cli.arguments.input))
                exit(1)

        else:
            # Download from Twitch API
            helix = twitch.Helix(client_id=app.config.settings['client_id'], use_cache=True)

            try:
                video: helix.Video = helix.video(video_id)
            except KeyError:
                print('Error: Invalid video or client id.')

            self.metadata: dict = api.video(video_id)
            self.comments = self.comment_generator_from_api(video)



    def __str__(self):
        return self.metadata['title']

    def __eq__(self, other):
        return self.id() == other.id()

    def id(self) -> str:
        return self.metadata['_id'].strip('v')

    @staticmethod
    def comment_generator_from_api(video: helix.Video) -> Generator[dict, None, None]:
        for comment in video.comments():
            yield comment.data

    @staticmethod
    def comment_generator(comments: List[dict]) -> Generator[dict, None, None]:
        for comment in comments:
            yield comment
