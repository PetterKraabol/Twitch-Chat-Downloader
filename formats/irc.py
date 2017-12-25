import app
import twitch
from formats import formatter, timestamp
from typing import Tuple, Generator, Union, List


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    output = formatter.format_output(app.settings['formats']['irc']['output'], video)
    return messages(video.comments), output


def messages(comments: Generator[dict, None, None]) -> Generator[str, None, None]:
    for comment in comments:

        # Timestamp
        comment['created_at'] = timestamp.use('%X', comment['created_at'])

        # Badges
        if 'user_badges' not in comment['message']:
            comment['message']['user_badges'] = [{'_id': '', 'version': 1}]

        comment['commenter']['badge'] = {
            'subscriber': '+',
            'moderator': '@',
            'global_mod': '%',
            'admin': '&',
            'staff': '!',
            'broadcaster': '~',
        }.get(comment['message']['user_badges'][0]['_id'], '')

        if comment['message']['is_action']:
            yield app.settings['formats']['irc']['comments']['action_format'].format(**comment)
        else:
            yield app.settings['formats']['irc']['comments']['format'].format(**comment)
