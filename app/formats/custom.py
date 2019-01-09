from typing import Tuple, Union, Generator

import twitch

from app.formats.format import Format
from app.pipe import Pipe


class Custom(Format):

    def __init__(self, video: twitch.helix.Video, format_dictionary: dict):
        super().__init__(video, format_dictionary)
        self.comment_pipe = Pipe(format_dictionary=format_dictionary['comments'])
        self.output_pipe = Pipe(format_dictionary=format_dictionary['output'])
        print('Custom')

    def use(self) -> Tuple[Generator[Union[Tuple[str, dict], dict], None, None], str]:
        return self.comment_generator(self.video.comments()), self.output_pipe.format_output(self.video.data)

    def comment_generator(self, comments: twitch.v5.Comments) -> Generator[Union[Tuple[str, dict], dict], None, None]:
        for comment in comments:
            yield self.comment_pipe.format_comment(comment.data)
