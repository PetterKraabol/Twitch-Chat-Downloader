#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, time, os, json, shutil, argparse, datetime

# Parse arguments
parser = argparse.ArgumentParser(description='Twitch Chat Downloader')
parser.add_argument('-v', '--video', help='Video id')
parser.add_argument('-i', '--client-id', help='Twitch client id')
parser.add_argument('-p', '--print', dest='p', help='Print messages', action='store_true')
parser.add_argument('-o', '--output', help='Output folder')
parser.add_argument('-f', '--format', help='Message format', choices=['timestamp', 'relative', 'srt', 'ssa', 'ass', 'raw'])
parser.add_argument('--cooldown', type=float, help='Cooldown time between API requests in seconds')
parser.add_argument('--start', type=int, help='Start time in seconds from video start')
parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')
parser.add_argument('--subtitle-duration', type=int, help='If using a subtitle format, subtitle duration in seconds')

arguments = parser.parse_args()

# Get video ID
if arguments.video:
    videoId = 'v' + arguments.video.replace('v', '')
else:
    videoId = 'v' + raw_input('Video ID: ').replace('v', '')

# Program requires at least example.setting.json or settings.json to run properly
if not os.path.isfile('example.settings.json') and not os.path.isfile('settings.json'):
    print 'Error: Missing settings file.'
    sys.exit(1)

# Copy settings example file if settings.json doesn't exist
if not os.path.isfile('settings.json'):
    shutil.copyfile('example.settings.json', 'settings.json')

# Load settings
with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

# Check settings version
if os.path.isfile('example.settings.json'):
    with open('example.settings.json', 'r') as example_settings_file:
        exampleSettings = json.load(example_settings_file)
        if 'version' not in settings:
            print '[Warning]\nYour settings.json file does not contain a version number. Compare settings.json to example.settings.json to make sure it\'s up to date.\n'

        elif 'version' in settings and settings['version'] != exampleSettings['version']:
            print '[Warning]\nYour settings.json file is outdated. Compare settings.json to example.settings.json.\nYour version: ' + settings['version'] + '\nNewest version: ' + exampleSettings['version'] + '\n'

# Check if a client_id was provided as an argument
if arguments.client_id:
    if not arguments.client_id == settings['client_id']:
        settings['client_id'] = arguments.client_id
        answer = raw_input('Save client ID? (Y/n): ')
        if (not answer.lower() == "n"):
            with open('settings.json', 'w') as settings_file:
                json.dump(settings, settings_file)

# Check if client_id is required
if settings['require_client_id'] and not settings['client_id']:
    print "Twitch requires a client ID to use their API.\nRegister an application on https://www.twitch.tv/settings/connections to get yours."
    settings['client_id'] = raw_input('Client ID: ')
    answer = raw_input('Save client ID? (Y/n): ')
    if (not answer.lower() == "n"):
        with open('settings.json', 'w') as settings_file:
            json.dump(settings, settings_file)

# Get client id parameter for URL
def getClientIdParameter():
    if (settings['client_id']):
        return 'client_id='+settings['client_id'] + '&'
    else:
        return ''

# Overwrite remaining settings with arguments
if arguments.p:
    settings['print'] = arguments.p

if arguments.format:
    settings['format'] = arguments.format

if arguments.cooldown:
    settings['cooldown'] = arguments.cooldown

if arguments.subtitle_duration:
    settings['subtitle_duration'] = arguments.subtitle_duration

# API URL
apiUrl = 'https://rechat.twitch.tv/rechat-messages'

# Get start and stop time by looking at the 'detail' message from Twitch
#
# If you query this API with invalid an invalid timestamp (none or out of range),
# it will tell you the start and stop timestamp, however, in text format.
response = requests.get(apiUrl + '?' + str(getClientIdParameter()) + 'start=0&video_id=' + videoId).json()

# Parse response for start and stop
#
# The response will look something like this
# {
#   "errors": [
#     {
#       "status": 400,
#       "detail": "0 is not between 1469108651 and 1469133795"
#     }
#   ]
# }
#
# As the start and stop timestamp is (for some weird reason)
# in text format, we have to parse the response.
detail = response['errors'][0]['detail'].split(' ') # We split the detail string into an array

# Check if valid video ID
# If the length is 8, it's (most likely) invalid
# If the length is 7, it's (most likely) valid
if len(detail) != 7:
    if settings['require_client_id']:
        print 'Error: Invalid video or client ID'
    else:
        print 'Error: Invalid video ID'
    sys.exit(1)

# Start and stop points
start = int(detail[4])    # The start timestamp is on index 4
stop = int(detail[6])     # while stop has the index 6

# Original start and stop
fullStart = start         # Keep original full-length start point
fullStop = stop           # Keep original full-length stop potin

# Used message ids
#
# Every message has an unique ID, which can be used for checking if we've already stored it.
messageIds = []

# Open output file
#
# This is where we save the messages.

# Output directory

if arguments.output:
    directory = arguments.output
else:
    directory = settings['output']

if not os.path.exists(directory):
    os.makedirs(directory)

# Open file (different file extension for subtitle formats)
if settings['format'] == 'srt' or settings['format'] == 'ssa' or settings['format'] == 'ass':
    file = open(directory + '/' + videoId + '.' + settings['format'], 'w')
elif settings['format'] == 'raw':
    file = open(directory + '/' + videoId + '.json', 'w')
else:
    file = open(directory + '/' + videoId + '.txt', 'w')

# Add format line if SSA/ASS subtitle format
if settings['format'] == 'ssa' or settings['format'] == 'ass':
    file.write('[Script Info]\n')
    file.write('Timer: 100,0000\n')

    file.write('\n[V4 Styles]\n')
    file.write(settings['ssa_style_format'] + '\n')
    file.write(settings['ssa_style_default']  + '\n')

    file.write('\n[Events]\n')
    file.write(settings['ssa_events_format'] + '\n')

# When saving as raw format (json), messages will be added to this
# object array and written to file after fetching all the messages
# to avoid opening, reading, writing to and closing the file for every
# message.
rawData = []

# Stop time argument
if arguments.stop and start + arguments.stop <= stop:
    stop = start + arguments.stop


# Start time argument
if arguments.start:
    start += arguments.start


# Download messages from timestamps between start and stop.
timestamp = start

while timestamp <= stop:

    # Wait for cooldown timer and request new messages from Twitch
    # The API returns the next 30 seconds of messages
    time.sleep(settings['cooldown'])
    response = requests.get(apiUrl + '?start=' + str(timestamp) + '&video_id=' + videoId).json()
    data = response['data'];

    # Increase timestamp to get the next 30 seconds of messages in the next loop
    timestamp += 30

    for message in data:

        # Timestamp for message (seconds)
        messageTimestampInSeconds = message['attributes']['timestamp']/1000.

        # Check the unique message ID to make sure it's not already saved.
        if not any(message['id'] in s for s in messageIds) and messageTimestampInSeconds <= stop:

            # If this is a new message, save the unique ID to prevent duplication later.
            messageIds.append(message['id'])
            date    = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime(messageTimestampInSeconds))
            sender  = message['attributes']['from'].encode('utf-8')
            color   = message['attributes']['color']
            text    = message['attributes']['message'].encode('utf-8')

            if color is None:
                color = 'FFFFFF'
            else:
                color = color.replace('#', '')

            # Timestamp format
            if settings['format'] == 'timestamp':
                line = date + ' ' + sender + ': ' + text + '\n'
                printLine = '\033[94m' + date + ' \033[92m'+ sender + '\033[0m' + ': ' + text

            # Relative timestamp format
            if settings['format'] == 'relative':
                line = str(datetime.timedelta(seconds=messageTimestampInSeconds - start)) + ' ' + sender + ': ' + text + '\n'
                printLine = '\033[94m' + str(datetime.timedelta(seconds=messageTimestampInSeconds-start)) + ' \033[92m'+ sender + '\033[0m' + ': ' + text

            # Subtitle formats
            if settings['format'] in {'srt', 'ass', 'ssa'}:
                subtitleStart = str(datetime.timedelta(seconds=messageTimestampInSeconds - start))
                subtitleStop = str(datetime.timedelta(seconds=messageTimestampInSeconds - start + settings['subtitle_duration']))

                # Bugfix - add milliseconds if missing
                # https://github.com/PetterKraabol/Twitch-Chat-Downloader/issues/3
                if len(subtitleStart) == 7:
                    subtitleStart += '.000000'

                if len(subtitleStop) == 7:
                    subtitleStop += '.000000'

                # srt format
                if settings['format'] == 'srt':
                    line = str(len(messageIds)) + '\n' + subtitleStart[:-3] + ' --> ' + subtitleStop[:-3] + '\n' + sender + ': ' + text + '\n\n'
                    printLine = printLine = '\033[94m' + subtitleStart + ' \033[92m'+ sender + '\033[0m' + ': ' + text

                # SSA/ASS format
                # Note: sender's color code is reversed for SSA and ASS format.
                if settings['format'] == 'ssa' or settings['format'] == 'ass':

                    # SSA/ASS expects BGR instead of RBG
                    BGRColor = color[4:6] + color[2:4] + color[0:2]

                    line = 'Dialogue: Marked=0, ' + subtitleStart[:-4] + ', ' + subtitleStop[:-4] + ', Default, ' + sender + ', 0000, 0000, 0000 , , {\c&H' + BGRColor + '&}' + sender + '{\c&HFFFFFF&}: ' + text + '\n'
                    printLine = printLine = '\033[94m' + str(datetime.timedelta(seconds=messageTimestampInSeconds - start)) + ' \033[92m'+ sender + '\033[0m' + ': ' + text


            if settings['format'] == 'raw':
                rawData.append(message)

            # Save messages to file unless saving raw data.
            # This is done after download all messages
            if settings['format'] != 'raw':
                file.write(line)

            # Print messages, if not, show progress
            if settings['print']:
                print printLine
            else:

                #Show progress %
                progress = round((timestamp - start)*100 / float(stop - start), 2)

                # Bugfix: progress can go slightly above 100% on the last loop
                if progress > 100.0:
                    progress = 100.0

                sys.stdout.write('Downloading ' + str(int(messageTimestampInSeconds - start)) + '/' + str(stop - start) + 's (' + str(progress) + '%) \r')
                sys.stdout.flush()

# If format is set to raw, save raw data
if settings['format'] == 'raw':
    file.write(json.dumps(rawData))

# Close file
file.close()
sys.stdout.write('Finished downloading ' + videoId + '\r')
