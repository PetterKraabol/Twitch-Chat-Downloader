import json
import shutil
import logging
from pathlib import Path

# Default example file
SETTINGS_EXAMPLE_FILE: str = 'settings.example.json'
SETTINGS_FILE: str = 'settings.json'


def read(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        logging.info('Loading configurations form ' + filename)
        return json.load(file)


def load(filename: str) -> dict:
    # Copy example file if necessary
    if not Path(filename).is_file():
        shutil.copyfile(SETTINGS_EXAMPLE_FILE, filename)

    # Load config files
    config_example: dict = read(SETTINGS_EXAMPLE_FILE)
    config: dict = read(filename)

    # Config versioning
    if config['version'][0] != config_example['version'][0]:
        logging.warning('Your settings file is deprecated. Using newest: v' + config_example['version'])
        return config_example
    elif config['version'] != config_example['version']:
        logging.warning('Please update your settings file to v' + config_example['version'])

    return config


def save(filename: str, data: dict):
    with open(filename, 'w') as file:
        json.dump(data, file)


settings: dict = load('settings.json')
