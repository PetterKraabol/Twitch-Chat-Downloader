import json
import pathlib
from typing import Optional, Dict, Any

from app.singleton import Singleton


class Settings(metaclass=Singleton):

    def __init__(self, filepath: Optional[str] = None, reference_filepath: Optional[str] = None):
        """
        Initialize settings with filepath and reference filepath
        :param filepath: Path to settings file
        :param reference_filepath: Path to reference settings file
        """
        if filepath is None:
            print('Settings filepath was not provided')
            exit(1)

        self.filepath = pathlib.Path(filepath)
        self.directory: pathlib.Path = self.filepath.parent
        self.reference_filepath = pathlib.Path(reference_filepath)

        self.config: Dict[str, Any] = self.load(filepath)

    def load(self, filepath: str) -> Dict[str, Any]:
        """
        Load dictionary from json file
        :param filepath: filepath to load from
        :return: Configuration dictionary
        """

        # Create settings file from reference file if necessary
        if not self.filepath.exists():
            self.directory.mkdir(exist_ok=True)

            # Missing reference file
            if not self.reference_filepath.exists():
                print(
                    'Missing settings reference. Available at https://github.com/PetterKraabol/Twitch-Chat-Downloader')
                exit(1)

            # Load config from reference settings
            with open(self.reference_filepath, 'r') as file:
                config = json.load(file)

            self.save(self.filepath, data=config)

            return config

        # Load from settings file
        try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print('Invalid settings format')
            exit(1)

    @staticmethod
    def save(filepath: str, data: dict) -> None:
        """
        Save configuration to settings file
        :param filepath: Filepath to save to
        :param data: Configuration dictionary to save
        :return: None
        """
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

    def update(self) -> None:
        """
        Update configuration settings and file using reference settings.
        :return: None
        """
        self.save('settings.{version}.backup.json').format(self.config['version'], self.config)
        new_config: dict = self.load(self.reference_filepath)

        # Copy client ID to new config file
        new_config['client_id'] = self.config['client_id']

        # Copy user-defined formats to new config file
        for format_name, format_dictionary in dict(self.config['formats']).items():
            if format_name not in new_config['formats']:
                new_config['formats'][format_name] = format_dictionary

        # Overwrite current config with new
        self.save(self.filepath, new_config)
        self.config = new_config
