import app
from pipe import mapper, reducer, filter
from typing import Tuple


# Formatting pipes

def comment(comment_input: dict, comment_format: dict) -> Tuple[str, dict]:
    mapper.use(comment_input, comment_format)

    return reducer.use(comment_input, comment_format)


def output(video_metadata: dict, output_format: dict) -> str:
    filter.output(video_metadata, output_format)
    mapper.use(video_metadata, output_format)

    # Ignore video metadata from reducer output
    output_string, _ = reducer.use(video_metadata, output_format)

    return '{}/{}'.format(app.arguments.output.rstrip('/').rstrip('\\'), output_string)
