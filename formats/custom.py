import twitch
import pipe
from typing import Generator, Tuple


def use(custom_format: dict, video: twitch.Video) -> Tuple[Generator[Tuple[str, dict], None, None], str]:
    return comment_generator(video.comments, custom_format['comments']), pipe.output(video.metadata,
                                                                                     custom_format['output'])


def comment_generator(comments: Generator[dict, None, None], comment_format: dict) -> Generator[Tuple[str, dict], None, None]:
    for comment in comments:
        yield pipe.comment(comment, comment_format)
