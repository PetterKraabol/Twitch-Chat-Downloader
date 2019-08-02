from typing import Optional, Dict, Union, List

from .singleton import Singleton


class Arguments(metaclass=Singleton):
    """
    Arguments singleton
    """

    class Name:
        SETTINGS_FILE: str = 'settings_file'
        SETTINGS: str = 'settings'
        INIT: str = 'init'
        VERBOSE: str = 'verbose'
        QUIET: str = 'quiet'
        PREVIEW: str = 'preview'
        FORMATS: str = 'formats'
        VERSION: str = 'version'
        OUTPUT: str = 'output'
        CLIENT_ID: str = 'client_id'
        CHANNEL: str = 'channel'
        USER: str = 'user'
        INCLUDES: str = 'includes'
        FIRST: str = 'first'
        VIDEO: str = 'video'
        FORMAT: str = 'format'
        TIMEZONE: str = 'timezone'
        DEBUG: str = 'debug'
        LOG: str = 'log'

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
        self.settings: str = arguments[Arguments.Name.SETTINGS]
        self.init: bool = arguments[Arguments.Name.INIT]
        self.verbose: bool = arguments[Arguments.Name.VERBOSE]
        self.debug: bool = arguments[Arguments.Name.DEBUG]
        self.quiet: bool = arguments[Arguments.Name.QUIET]
        self.preview: bool = arguments[Arguments.Name.PREVIEW]
        self.print_formats: bool = arguments[Arguments.Name.FORMATS]
        self.print_version: bool = arguments[Arguments.Name.VERSION]
        self.output: str = arguments[Arguments.Name.OUTPUT]
        self.log: bool = arguments[Arguments.Name.LOG]

        # Optional or prompted arguments
        self.client_id: Optional[str] = arguments[Arguments.Name.CLIENT_ID]
        self.first: Optional[int] = arguments[Arguments.Name.FIRST]
        self.timezone: Optional[str] = arguments[Arguments.Name.TIMEZONE]
        self.includes: Optional[str] = arguments[Arguments.Name.INCLUDES]

        # Arguments that require some formatting
        self.video_ids: List[int] = []
        self.formats: List[str] = []
        self.channels: List[str] = []
        self.users: List[str] = []

        # Videos
        if arguments[Arguments.Name.VIDEO]:
            self.video_ids = [int(video_id) for video_id in arguments[Arguments.Name.VIDEO].lower().split(',')]

        # Formats
        if arguments[Arguments.Name.FORMAT]:
            self.formats: Optional[List[str]] = arguments[Arguments.Name.FORMAT].lower().split(',')

        # Channels
        if arguments[Arguments.Name.CHANNEL]:
            self.channels = arguments[Arguments.Name.CHANNEL].lower().split(',')

        # Users
        if arguments[Arguments.Name.USER]:
            self.users = arguments[Arguments.Name.USER].lower().split(',')
