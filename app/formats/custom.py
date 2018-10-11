import app.twitch as twitch
import app.pipe as pipe
from typing import Generator, Tuple


def use(custom_format: dict, video: twitch.Video) -> Tuple[Generator[Tuple[str, dict], None, None], str]:
    # Format comments
    comments: Generator[Tuple[str, dict], None, None] = comment_generator(video.comments, custom_format['comments'])

    # Format output
    output = pipe.output(video.metadata, custom_format['output'])

    return comments, output


def comment_generator(comments: Generator[dict, None, None],
                      comment_format: dict) -> Generator[Tuple[str, dict], None, None]:
    for comment in comments:
        yield pipe.comment(comment, comment_format), comment
