import pathlib
from typing import Optional, Dict, Union, List

from app.singleton import Singleton


class Arguments(metaclass=Singleton):
    """
    Arguments singleton
    """

    class Name:
        SETTINGS_FILE: str = 'settings'
        INIT: str = 'init'
        VERBOSE: str = 'verbose'
        QUIET: str = 'quiet'
        PREVIEW: str = 'preview'
        FORMATS: str = 'formats'
        VERSION: str = 'version'
        UPDATE: str = 'update'
        OUTPUT: str = 'output'
        CLIENT_ID: str = 'client_id'
        CHANNEL: str = 'channel'
        FIRST: str = 'first'
        VIDEO: str = 'video'
        FORMAT: str = 'format'
        TIMEZONE: str = 'timezone'
        START: str = 'start'
        STOP: str = 'stop'
        INPUT: str = 'input'
        DEBUG: str = 'debug'

    def __init__(self, arguments: Optional[Dict[str, Union[str, bool, int]]] = None):
        """
        Initialize arguments
        :param arguments: Arguments from cli (Optional to call singleton instance without parameters)
        """

        if arguments is None:
            print('Error: arguments were not provided')
            exit()

        # Required arguments and booleans
        self.settings_file: str = arguments[Arguments.Name.SETTINGS_FILE]
        self.init: bool = arguments[Arguments.Name.INIT]
        self.verbose: bool = arguments[Arguments.Name.VERBOSE]
        self.debug: bool = arguments[Arguments.Name.DEBUG]
        self.quiet: bool = arguments[Arguments.Name.QUIET]
        self.preview: bool = arguments[Arguments.Name.PREVIEW]
        self.print_formats: bool = arguments[Arguments.Name.FORMATS]
        self.print_version: bool = arguments[Arguments.Name.VERSION]
        self.update: bool = arguments[Arguments.Name.UPDATE]
        self.output: str = arguments[Arguments.Name.OUTPUT]

        # Optional or prompted arguments
        self.client_id: Optional[str] = arguments[Arguments.Name.CLIENT_ID]
        self.first: Optional[int] = arguments[Arguments.Name.FIRST]
        self.timezone: Optional[str] = arguments[Arguments.Name.TIMEZONE]
        self.start: Optional[int] = arguments[Arguments.Name.START]
        self.stop: Optional[int] = arguments[Arguments.Name.STOP]

        # Arguments that require some formatting
        self.video_ids: List[int] = []
        self.formats: List[str] = []
        self.channels: List[str] = []
        self.input: Optional[pathlib.Path] = None

        if arguments[Arguments.Name.VIDEO]:
            self.video_ids = [int(video_id) for video_id in arguments[Arguments.Name.VIDEO].lower().split(',')]

        if arguments[Arguments.Name.FORMAT]:
            self.formats: Optional[List[str]] = arguments[Arguments.Name.FORMAT].lower().split(',')

        if arguments[Arguments.Name.CHANNEL]:
            self.channels = arguments[Arguments.Name.CHANNEL].lower().split(',')

        if arguments[Arguments.Name.INPUT]:
            self.input = pathlib.Path(arguments[Arguments.Name.INPUT])

    @staticmethod
    def prompt_video_id() -> str:
        """
        Prompt for video ID if necessary
        :return: Video ID
        """
        return input('Video ID(s): ').strip()

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
