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
        return prompt_update(config, config_example)

    return config


def save(filename: str, data: dict):
    """
    Convert config dictionary to file and save to file.
    :param filename: Output filename
    :param data: Config dictionary
    :return:
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def prompt_update(current_config: dict, new_config: dict) -> dict:
    print('Your settings file is outdated ({}). Please update to {}'.format(current_config['version'],
                                                                            new_config['version']))

    answer = input('Update to new version? Existing settings will be backed up. (Y/n): ')
    if answer.lower().startswith('n'):
        exit(1)
    else:
        return update(current_config, new_config)


def update(current_config: dict, new_config: dict) -> dict:
    save('settings.{}.backup.json'.format(current_config['version']), current_config)

    # Copy client id to new config file
    new_config['client_id'] = current_config['client_id']

    # Copy user-defined formats to new config file
    for format_name, format_dictionary in dict(current_config['formats']).items():
        if format_name not in new_config['formats']:
            new_config['formats'][format_name] = format_dictionary

    # Overwrite current config file with new config.
    save(SETTINGS_FILE, new_config)

    return new_config


settings: dict = load('settings.json')
