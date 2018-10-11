from typing import Generator

import requests

import app.cli
import app.config


def get(path: str, params: dict = None, headers: dict = None) -> requests.Response:
    params = {} if params is None else params
    headers = {} if headers is None else headers
    params['client_id'] = app.config.settings['client_id']

    response: requests.Response = requests.get(url=str(app.config.settings['twitch_api']).format(path=path),
                                               params=params,
                                               headers=headers)
    if response.status_code != requests.codes.ok:
        print('\n[Error]')
        print('Twitch API returned status code {}. Please check your client ID.'.format(response.status_code))
        print('\nUrl\t{}\nParams\t{}\nHeaders\t{}\n'.format(response.url, params, headers))
        exit(1)
    return response


def video(video_id: str) -> dict:
    if app.cli.arguments.verbose:
        print('Downloading video metadata from Twitch API')
    return get('videos/{}'.format(video_id)).json()


def comment_fragment(video_id: str, cursor: str = '') -> dict:
    return get('videos/{}/comments'.format(video_id), {'cursor': cursor}).json()


def comments(video_id: str) -> Generator[dict, None, None]:
    if app.cli.arguments.verbose:
        print('Downloading comments from Twitch API')

    fragment: dict = {'_next': ''}

    while '_next' in fragment:
        fragment = comment_fragment(video_id, fragment['_next'])
        for comment in fragment['comments']:
            yield comment
