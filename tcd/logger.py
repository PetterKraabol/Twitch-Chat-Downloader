import time
from typing import List

from .arguments import Arguments
from .singleton import Singleton


class Log:
    DEBUG: str = 'debug'
    ERROR: str = 'error'
    REGULAR: str = 'regular'
    CRITICAL: str = 'critical'
    VERBOSE: str = 'verbose'
    PREVIEW: str = 'preview'
    PROGRESS: str = 'progress'

    def __init__(self, message: str = '', log_type: str = REGULAR):
        self.message: str = message
        self.type: str = log_type
        self.timestamp: float = time.time()

    def __str__(self) -> str:
        if self.type == Log.CRITICAL:
            return f'[Critical]: {self.message}'

        if self.type == Log.DEBUG:
            return f'[Debug]: {self.message}'

        return self.message

    def full(self) -> str:
        """
        Return full log message with timestamp, type and message
        :return:
        """
        return '{} [{}]: {}'.format(self.timestamp, self.type, self.message)


class Logger(metaclass=Singleton):

    def __init__(self):
        self.logs: List[Log] = []

    def log(self, message: str = '', log_type: str = Log.REGULAR, retain: bool = True) -> None:
        """
        Log a message
        :param message: Log message
        :param log_type: Log type
        :param retain: Save log to memory
        :return: None
        """
        # Add log to
        log = Log(message, log_type)

        # Save log entry to memory
        if retain and log.type is not Log.PREVIEW:
            self.logs.append(log)

        if self.should_print(log.type):
            print(log)

    @staticmethod
    def should_print(log_type: str) -> bool:
        """
        Check if log should be printed
        :param log_type: Log type
        :return: Whether to print the log
        """
        # Critical (always print)
        if log_type == Log.CRITICAL:
            return True

        # Quiet (only critical)
        if Arguments().quiet:
            return False

        # Progress - default output
        if log_type == Log.PROGRESS and (Arguments().debug or Arguments().verbose or Arguments().preview):
            return False

        # Debug
        if log_type == Log.DEBUG and not Arguments().debug:
            return False

        # Verbose
        if log_type == Log.VERBOSE and not Arguments().verbose:
            return False

        # Preview
        if log_type == Log.PREVIEW and not Arguments().preview:
            return False

        return True

    def save(self, filename: str = 'tcd.log') -> None:
        """
        Save retained logs to file
        :param filename: File to save to
        :return: None
        """
        with open(filename, 'w') as file:
            [file.write('{}\n'.format(log.full())) for log in self.logs]
