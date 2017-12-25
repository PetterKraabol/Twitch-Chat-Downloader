import app
import twitch
from formats import formatter
from typing import Tuple, Generator, List, Union


def use(video: twitch.Video) -> Tuple[Generator[dict, None, None], str]:
    print('Downloading JSON data...')

    output = formatter.format_output(app.settings['formats']['json']['output'], video)

    json_object = dict()
    json_object['video']: dict = video.metadata
    json_object['comments']: List[dict] = []

    for comment in video.comments:
        json_object['comments'].append(comment)

    return generator(json_object), output


def generator(json_object: dict) -> Generator[dict, None, None]:
    yield json_object
