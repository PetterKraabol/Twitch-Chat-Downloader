import json
import shutil
from pathlib import Path

SETTINGS_EXAMPLE_FILE: str = 'settings.example.json'
SETTINGS_FILE: str = 'settings.json'


def read(filename: str) -> dict:
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def load(filename: str) -> dict:
    # Copy example file if necessary
    if not Path(filename).is_file():
        shutil.copyfile(SETTINGS_EXAMPLE_FILE, filename)

    # Load config files
    config_example: dict = read(SETTINGS_EXAMPLE_FILE)
    config: dict = read(filename)

    # Config versioning and updating
    if config['version'] != config_example['version']:
        print('Your settings file is outdated ({}). Please update to {}'.format(config['version'],
                                                                                config_example['version']))

        answer = input('Update to new version? Existing settings will be backed up. (y/N): ')
        if answer.lower() == 'y':
            save('settings.{}.backup.json'.format(config['version']), config)

            # Copy client id to new config file
            config_example['client_id'] = config['client_id']

            # Copy user-defined formats to new config file
            for format_name, format_dictionary in dict(config['formats']).items():
                if format_name not in config_example['formats']:
                    config_example[format_name] = format_dictionary

            save(SETTINGS_FILE, config_example)
            return config_example
        else:
            exit(1)

    return config


def save(filename: str, data: dict):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


settings: dict = load('settings.json')
