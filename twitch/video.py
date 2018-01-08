import json
import app.cli
import twitch.api
from typing import List, Generator
from pathlib import Path


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
            self.metadata: dict = twitch.api.video(video_id)
            self.comments = twitch.api.comments(video_id)

    def __str__(self):
        return self.metadata['title']

    def __eq__(self, other):
        return self.id() == other.id()

    def id(self) -> str:
        return self.metadata['_id'].strip('v')

    @staticmethod
    def comment_generator(comments: List[dict]) -> Generator[dict, None, None]:
        for comment in comments:
            yield comment
