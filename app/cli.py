import argparse

import app.config


# Ask for video ID
def prompt_video_id() -> str:
    return input('Video ID: ').strip('v').strip()


# Ask for Twitch client ID
def prompt_client_id(initialize: bool = False):
    print('Twitch requires a client ID to use their API.'
          '\nRegister an application on https://dev.twitch.tv/dashboard to get yours.')
    app.config.settings['client_id'] = input('Client ID: ').strip()
    if initialize:
        app.config.save(app.config.SETTINGS_FILE, app.config.settings)
    else:
        answer: str = input('Save client ID? (Y/n): ').strip().lower()
        if not answer.startswith('n'):
            app.config.save(app.config.SETTINGS_FILE, app.config.settings)


# Arguments
parser: argparse.ArgumentParser = argparse.ArgumentParser(
    description='Twitch Chat Downloader v{version}'.format(version=app.config.settings['version']))

parser.add_argument('-v', '--video', type=str, help='Video id')
# parser.add_argument('-c', '--channel', type=str, help='Channel name')
# parser.add_argument('--limit', type=int, help='Number of videos from channel')
parser.add_argument('--client_id', type=str, help='Twitch client id')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('-q', '--quiet', action='store_true')
parser.add_argument('-o', '--output', type=str, help='Output folder', default='./output')
parser.add_argument('-f', '--format', type=str, help='Message format', default='default')
# parser.add_argument('--start', type=int, help='Start time in seconds from video start')
# parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')
parser.add_argument('--timezone', type=str, help='Timezone name')
parser.add_argument('--init', action='store_true', help='Script setup')
parser.add_argument('--update', action='store_true', help='Update settings')
parser.add_argument('--version', action='store_true', help='Settings version')
parser.add_argument('--formats', action='store_true', help='List available formats')
parser.add_argument('--preview', action='store_true', help='Print chat lines')
parser.add_argument('--input', type=str, help='Read data from JSON file')

arguments = parser.parse_args()

# Turn format to lowercase
arguments.format = str(arguments.format).lower()

# Initialize
if arguments.init:
    prompt_client_id(initialize=True)
    print('Twitch Chat Downloader has been initialized.')
    exit(1)

# Update
if arguments.update:
    print('You are up to date with v{}'.format(app.config.settings['version']))
    exit(1)

# Version
if arguments.version:
    print('Twitch Chat Downloader v{version}'.format(version=str(app.config.settings['version'])))
    exit(1)

# List formats
if arguments.formats:
    for format_name in app.config.settings['formats']:
        print(format_name)
        _format = app.config.settings['formats'][format_name]
        if 'comments' in _format:
            print('\tcomment: {}'.format(app.config.settings['formats'][format_name]['comments']['format']))
        if 'output' in _format:
            print('\toutput: {}'.format(app.config.settings['formats'][format_name]['output']['format']))
        print('\n')

    exit(1)

# Video ID
if arguments.video is None and arguments.input is None:
    arguments.video = prompt_video_id()

# Client ID
if app.config.settings['client_id'] is None and arguments.client_id is None:
    prompt_client_id()

# Client ID argument
if arguments.client_id:
    if app.config.settings['client_id'] is not arguments.client_id:
        app.config.settings['client_id'] = str(arguments.client_id).strip()
        save: str = input('Save client ID? (Y/n): ').strip().lower()
        if not save.startswith('n'):
            app.config.save(app.config.SETTINGS_FILE, app.config.settings)

