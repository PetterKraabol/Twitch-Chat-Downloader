import app
import twitch
from formats import formatter
from typing import Tuple, Generator
from itertools import chain


def use(video: twitch.Video) -> Tuple[Generator[str, None, None], str]:
    output = formatter.format_output(app.settings['formats']['srt']['output'], video)

    return messages(video.comments), output


def messages(comments: Generator[dict, None, None]) -> Generator[str, None, None]:
    for comment in comments:
        badges = comment_badges(comment)
        print(badges)
        yield 'todo: irc'
        #yield app.settings['formats']['irc']['comments'].format(comment)


def comment_badges(comment: dict) -> str:
    if 'user_badges' in comment['message']:
        return comment['message']['user_badges']
