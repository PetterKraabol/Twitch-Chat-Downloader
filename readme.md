# Twitch Chat Downloader

### Requirements
- [Python 2.7](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- ```pip install requests``` [Requests library installation guide](http://docs.python-requests.org/en/master/user/install/)

### Usage
```bash
$ python app.py 3456789
```
*Now, just replace the number with any video id, found in the url of the vod.*

### Important
- This script is using Twitch's unofficial and undocumented ReChat API. The script may break at any time.
- [As of August 8th 2016](https://discuss.dev.twitch.tv/t/client-id-requirement-faqs/6108), Twitch will require a client-id to be sent with every API calls. This may not affect the ReChat API.
- The longer VOD, the more API calls are made to Twitch (maybe thousands). Use with care and keep up to date on any rate limits.