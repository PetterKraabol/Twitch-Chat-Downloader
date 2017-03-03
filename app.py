#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, time, os, json, shutil, argparse, datetime

# Parse arguments
parser = argparse.ArgumentParser(description='Twitch Chat Downloader')
parser.add_argument('-v', '--video', help='Video id')
parser.add_argument('-i', '--client-id', help='Twitch client id')
parser.add_argument('-p', '--print', dest='p', help='Print messages', action='store_true')
parser.add_argument('-o', '--output', help='Output folder')
parser.add_argument('-f', '--format', help='Message format', choices=['timestamp', 'relative', 'srt', 'ssa', 'ass'])
parser.add_argument('--cooldown', type=float, help='Cooldown time between API requests in seconds')
parser.add_argument('--start', type=int, help='Start time in seconds from video start')
parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')

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
else:
    file = open(directory + '/' + videoId + '.txt', 'w')

# Add format line if SSA/ASS subtitle format
if settings['format'] == 'ssa' or settings['format'] == 'ass':
    file.write('Format: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')

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
        message['time'] = message['attributes']['timestamp']/1000.

        # Check the unique message ID to make sure it's not already saved.
        if not any(message['id'] in s for s in messageIds) and message['time'] <= stop:

            # If this is a new message, save the unique ID to prevent duplication later.
            messageIds.append(message['id'])
            date    = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime(message['time']))
            sender  = message['attributes']['from'].encode('utf-8')
            text    = message['attributes']['message'].encode('utf-8')

            # Timestamp format
            if settings['format'] == 'timestamp':
                line = date + ' ' + sender + ': ' + text + '\n'
                printLine = '\033[94m' + date + ' \033[92m'+ sender + '\033[0m' + ': ' + text

            # Relative timestamp format
            if settings['format'] == 'relative':
                line = str(datetime.timedelta(seconds=message['time'] - start)) + ' ' + sender + ': ' + text + '\n'
                printLine = '\033[94m' + str(datetime.timedelta(seconds=message['time']-start)) + ' \033[92m'+ sender + '\033[0m' + ': ' + text

            # srt format
            if settings['format'] == 'srt':
                line = str(len(messageIds)) + '\n' + str(datetime.timedelta(seconds=message['time'] - start))[:-3] + ' --> ' + str(datetime.timedelta(seconds=message['time'] - start + 2))[:-3] + '\n' + sender + ': ' + text + '\n\n'
                printLine = printLine = '\033[94m' + str(datetime.timedelta(seconds=message['time']-start)) + ' \033[92m'+ sender + '\033[0m' + ': ' + text

            # SSA/ASS format
            if settings['format'] == 'ssa' or settings['format'] == 'ass':
                line = 'Dialogue: Marked=0,' + str(datetime.timedelta(seconds=message['time'] - start))[:-4] + ',' + str(datetime.timedelta(seconds=message['time'] - start + 2))[:-4] + ',Wolf main,' + sender + ',0000,0000,0000,,' + sender + ': ' + text + '\n'
                printLine = printLine = '\033[94m' + str(datetime.timedelta(seconds=message['time']-start)) + ' \033[92m'+ sender + '\033[0m' + ': ' + text

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

                sys.stdout.write('Downloading ' + str(int(message['time'] - start)) + '/' + str(stop - start) + 's (' + str(progress) + '%) \r')
                sys.stdout.flush()

# Close file
file.close()
sys.stdout.write('Finished downloading ' + videoId + '\r')
