import app.config
import requests
import logging
from typing import Generator


def get(path: str, params: dict = None, headers: dict = None) -> requests.Response:
    params = {} if params is None else params
    headers = {} if headers is None else headers
    params['client_id'] = app.config.settings['client_id']

    response: requests.Response = requests.get(url=str(app.config.settings['twitch_api']).format(path=path),
                                               params=params,
                                               headers=headers)
    if response.status_code != requests.codes.ok:
        logging.warning('{} {} with {}'.format(response.status_code, response.url, params))

    return response


def video(video_id: str) -> dict:
    return get('videos/{}'.format(video_id)).json()


def comment_fragment(video_id: str, cursor: str = '') -> dict:
    return get('videos/{}/comments'.format(video_id), {'cursor': cursor}).json()


def comments(video_id: str) -> Generator[dict, None, None]:
    fragment: dict = {'_next': ''}

    while '_next' in fragment:
        fragment = comment_fragment(video_id, fragment['_next'])
        for comment in fragment['comments']:
            yield comment
