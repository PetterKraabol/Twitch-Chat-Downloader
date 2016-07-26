#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, sys, time, os


# Video id input (prefixed 'v' in the parameter is is optional).
videoId = 'v' + sys.argv[1].replace('v', '')

# Get start and stop time by looking at the 'detail' message from Twitch
#
# If you query this API with invalid an invalid timestamp (none or out of range),
# it will tell you the start and stop timestamp, however, in text format.
response = requests.get('https://rechat.twitch.tv/rechat-messages?start=0&video_id=' + videoId).json()

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
start = int(detail[4])                              # The start timestamp is on index 4
stop = int(detail[6])                               # while stop has the index 6

# Used message ids
#
# Every message has an unique ID, which we can check if we've already stored it.
# Querying a specific timestamp will not just return messages form that timestamp,
# but also messages that has been sent a few seconds after as well.
# I'm not sure what the time frame is.
messageIds = []

# Open output file
#
# This is where we save the messages.

# Output directory
directory = 'chats'
if not os.path.exists(directory):
    os.makedirs(directory)

# Filename
file = open(directory + '/' + videoId + '.txt', 'w')


# Download messages from timestamps between start and stop.
timestamp = start
while timestamp <= stop:

    # Request messages from Twitch
    response = requests.get('https://rechat.twitch.tv/rechat-messages?start=' + str(timestamp) + '&video_id=' + videoId).json()
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

            # Set timestamp to this message's timestamp to improve
            # performance and skip timestamps where no new messages are coming in.
            #
            # Note: The message timestamp is divided by 1000 because the ReChat API
            # query does not want the last 3 digits (for whatever reason)
            timestamp = int(message['attributes']['timestamp']/1000)

            # Print to console (optional)
            print '\033[94m' + date + ' \033[92m'+ sender + '\033[0m' + ': ' + text

# Close file
file.close()