import argparse
import app.config

format_types = app.config.settings['formats']

parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Twitch Chat Downloader')
parser.add_argument('-v', '--video', type=str, help='Video id')
parser.add_argument('--client_id', type=str, help='Twitch client id', default=None)
# parser.add_argument('--verbose', action='store_true')
parser.add_argument('-q', '--quiet', action='store_true')
parser.add_argument('-o', '--output', type=str, help='Output folder', default='./output')
parser.add_argument('-f', '--format', type=str, help='Message format', default='default')
# parser.add_argument('--start', type=int, help='Start time in seconds from video start')
# parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')
# parser.add_argument('--subtitle-duration', type=int, help='If using a subtitle format, subtitle duration in seconds')
parser.add_argument('--timezone', type=str, help='Timezone name', default=None)

arguments = parser.parse_args()

# Fix format
arguments.format = str(arguments.format).lower()

# Video ID
if arguments.video is None:
    answer: str = input('Video ID: ')
    arguments.video = answer.strip('v')

# Twitch client ID
if not app.config.settings['client_id'] and arguments.client_id is None:
    print('Twitch requires a client ID to use their API.'
          '\nRegister an application on https://dev.twitch.tv/dashboard to get yours.')
    app.config.settings['client_id'] = input('Client ID: ')
    answer: str = input('Save client ID? (Y/n): ')
    if answer.lower() != "n":
        app.config.save(app.config.SETTINGS_FILE, app.config.settings)
