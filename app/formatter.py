from typing import Generator, Tuple, Union

from twitch import helix

from app.formats.custom import Custom
from app.settings import Settings


class Formatter:

    def __init__(self, video: helix.Video):
        self.video: helix.Video = video

    def use(self, format_name: str) -> Tuple[Generator[Union[Tuple[str, dict], dict], None, None], str]:
        """
        Use format based on name
        :param format_name: Format name
        :return: Formatted comments and output name
        """

        # Check valid format name
        if format_name not in Settings().config['formats']:
            print('Invalid format name')
            exit(1)

        format_dictionary: dict = Settings().config['formats'][format_name]

        if format_name == 'json':
            return self.json()
        elif format_name == 'srt':
            return self.srt()
        elif format_name == 'ssa':
            return self.ssa()
        else:
            return Custom(self.video, format_dictionary).use()

    def json(self) -> Tuple[Generator[Union[Tuple[str, dict], dict], None, None], str]:
        pass

    def srt(self) -> Tuple[Generator[Union[Tuple[str, dict], dict], None, None], str]:
        pass

    def ssa(self) -> Tuple[Generator[Union[Tuple[str, dict], dict], None, None], str]:
        pass
