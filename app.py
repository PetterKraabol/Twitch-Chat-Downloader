#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, time, os, json, shutil

# Get video ID
if len(sys.argv) >= 2:
    videoId = 'v' + sys.argv[1].replace('v', '')
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
if len(sys.argv) >= 3:
    if not sys.argv[2] == settings['client_id']:
        settings['client_id'] = sys.argv[2]
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

start = int(detail[4])                              # The start timestamp is on index 4
stop = int(detail[6])                               # while stop has the index 6

# Used message ids
#
# Every message has an unique ID, which can be used for checking if we've already stored it.
# Querying a specific timestamp will not just return messages from that timestamp,
# but also messages that has been sent a few seconds after as well.
# I'm not sure what the time frame is.
messageIds = []

# Open output file
#
# This is where we save the messages.

# Output directory
directory = settings['folder']
if not os.path.exists(directory):
    os.makedirs(directory)

# Filename
file = open(directory + '/' + videoId + '.txt', 'w')


# Download messages from timestamps between start and stop.
timestamp = start
while timestamp <= stop:

    # Request messages from Twitch
    response = requests.get(apiUrl + '?start=' + str(timestamp) + '&video_id=' + videoId).json()
    data = response['data'];

    # Increase by one (will be overwritten if new messages are found).
    timestamp += 1

    for message in data:

        # Check the unique message ID to make sure it's not already saved.
        if not any(message['id'] in s for s in messageIds):

            # If this is a new message, save the unique ID to prevent duplication later.
            messageIds.append(message['id'])

            # Message data
            date    = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(message['attributes']['timestamp']/1000.))
            sender  = message['attributes']['from'].encode('utf-8')
            text    = message['attributes']['message'].encode('utf-8')

            # Append message to output file
            file.write(date + ' ' + sender + ': ' + text + '\n')

            # Print messages, if not, show progress
            if settings['print']:

                # Print messages
                print '\033[94m' + date + ' \033[92m'+ sender + '\033[0m' + ': ' + text
            else:

                #Show progress %
                progress = timestamp - start
                done = stop - start
                percentage = round(progress*100 / float(done), 2)

                # Bigfix: percentage goes slightly above 100
                if percentage > 100.0:
                    percentage = 100.0

                sys.stdout.write('Downloading... (' + str(percentage) + '%)\r')
                sys.stdout.flush()

            # Set timestamp to this message's timestamp to improve
            # performance and skip timestamps where no new messages are coming in.
            #
            # Note: The message timestamp is divided by 1000 because the ReChat API
            # query does not want the last 3 digits (for whatever reason)
            timestamp = int(message['attributes']['timestamp']/1000)

# Close file
file.close()
sys.stdout.write('Finished downloading ' + videoId + '\r')
