from typing import Generator, Tuple

import twitch

from tcd.formats.format import Format
from tcd.pipe import Pipe


class Custom(Format):

    def __init__(self, video: twitch.helix.Video, format_name: str):
        super().__init__(video, format_name)

    def use(self) -> Tuple[Generator[Tuple[str, twitch.v5.Comment], None, None], str]:
        """
        Use this format
        :return: tuple(formatted comment, comment), output format
        """
        # Format comments
        comments = self.comment_generator(self.video.comments())

        # Format output
        output: str = Pipe(self.format_dictionary['output']).output(self.video.data)

        return comments, output

    def comment_generator(self, comments: twitch.v5.Comments) -> Generator[Tuple[str, twitch.v5.Comment], None, None]:
        for comment in comments:
            yield Pipe(self.format_dictionary['comments']).comment(comment.data), comment
