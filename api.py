import requests
import logging
import config


def get(path: str, params: dict = None, headers: dict = None) -> requests.Response:
    if params is None:
        params = {}

    if headers is None:
        headers = {}

    params['client_id'] = config.settings['client_id']

    response: requests.Response = requests.get(url=str(config.settings['twitch_api']).format(path=path),
                                               params=params,
                                               headers=headers)
    if response.status_code != requests.codes.ok:
        logging.warning('{} {} with {}'.format(response.status_code, response.url, params))

    return response


def video(video_id: str) -> dict:
    return get('videos/{}'.format(video_id)).json()


def comment_fragment(video_id: str, cursor: str = '') -> dict:
    return get('videos/{}/comments'.format(video_id), {'cursor': cursor}).json()


def comments(video_id: str) -> dict:
    fragment: dict = {'_next': ''}

    while '_next' in fragment:
        fragment = comment_fragment(video_id, fragment['_next'])
        for comment in fragment['comments']:
            yield comment
