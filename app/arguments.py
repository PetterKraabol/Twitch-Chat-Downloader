import pathlib
from typing import Optional, Dict, Any

from app.singleton import Singleton


class Arguments(metaclass=Singleton):
    """
    Arguments singleton
    """

    def __init__(self, arguments: Optional[Dict[str, Any]] = None):
        """
        Initialize arguments
        :param arguments: Arguments from cli (Optional to call singleton instance without parameters)
        """

        if arguments is None:
            print('Error: arguments were not provided')
            exit(1)

        # Required arguments and booleans
        self.settings_file: str = arguments['settings']
        self.init: bool = arguments['init']
        self.verbose: bool = arguments['verbose']
        self.quiet: bool = arguments['quiet']
        self.preview: bool = arguments['preview']
        self.formats: bool = arguments['formats']
        self.version: bool = arguments['version']
        self.update: bool = arguments['update']
        self.output: str = arguments['output']

        # Optional or prompted arguments
        self.client_id: str = str(arguments['client_id']) or None
        self.channel: str = str(arguments['channel']).lower() or None
        self.limit: int = arguments['limit'] or None
        self.video: str = arguments['video'] or None
        self.format: str = str(arguments['format']).lower() or None
        self.timezone: str = arguments['timezone'] or None
        self.start: int = arguments['start'] or None
        self.stop: int = arguments['stop'] or None
        self.input = pathlib.Path(arguments['input']) if arguments['input'] else None

    @staticmethod
    def prompt_video_id() -> str:
        """
        Prompt for video ID if necessary
        :return: Video ID
        """
        return input('Video ID: ').strip()

    @staticmethod
    def prompt_client_id() -> str:
        """
        Prompt user for a client ID and ask to save it to file
        :return: Client ID
        """

        # Todo: move to Settings?
        print('Twitch requires a client ID to use their API.'
              '\nRegister an application on https://dev.twitch.tv/dashboard to get yours.')
        client_id: str = input('Client ID: ').strip()

        # todo: ask for overwrite and overwrite anyway if init

        return client_id
