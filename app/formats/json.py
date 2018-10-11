from typing import Tuple, Generator, List

import app
import app.pipe as pipe
import app.twitch as twitch


def use(video: twitch.Video) -> Tuple[Generator[dict, None, None], str]:
    # Send video through pipe to generate output
    output: str = pipe.output(video.metadata, app.settings['formats']['json']['output'])

    json_object = dict()
    json_object['video']: dict = video.metadata
    json_object['comments']: List[dict] = []

    # Download every comment and add to comments list
    for comment in video.comments:

        # Draw progress
        if not app.arguments.quiet and not app.arguments.verbose:
            app.draw_progress(comment['content_offset_seconds'], video.metadata['length'], 'json')

        # Append to comments
        json_object['comments'].append(comment)

    # Transform json object to a generator
    return generator(json_object), output


# Simply yield the json object once
def generator(json_object: dict) -> Generator[dict, None, None]:
    yield json_object
