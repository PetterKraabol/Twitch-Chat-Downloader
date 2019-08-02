import time
from datetime import datetime
from typing import List, Optional

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
        self.message: str = message.strip()
        self.type: str = log_type
        self.timestamp: str = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self) -> str:
        if self.type in [Log.DEBUG, Log.ERROR, Log.CRITICAL]:
            return f'[{self.type.capitalize()}: {self.message}]'

        return self.message

    def full(self) -> str:
        """
        Return full log message with timestamp, type and message
        :return:
        """
        return '{} [{}]: {}'.format(self.timestamp, self.type, self.message)


class Logger(metaclass=Singleton):

    def __init__(self, logs: Optional[List[Log]] = None):
        self.logs: List[Log] = logs or []

    def log(self, message: str = '', log_type: str = Log.REGULAR, retain: bool = True) -> Log:
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

            # Save log when debugging
            if Arguments().log:
                self.save()

        # Print
        if self.should_print_type(log.type):
            print(log)

        return log

    @staticmethod
    def should_print_type(log_type: str) -> bool:
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
        if log_type == Log.PROGRESS and (Arguments().verbose or Arguments().preview):
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
