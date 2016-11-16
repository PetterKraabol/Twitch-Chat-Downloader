# Twitch Chat Downloader

Neat python script to download chat messages from past broadcasts

### Requirements

- [Python 2.7](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [Requests library installation guide](http://docs.python-requests.org/en/master/user/install/)

### Install requirements
```bash
pip install -r requirements.txt
```

### Usage

```bash
python app.py 80123392
```
*Now, just replace the number with any video id, found in the url of the vod.*

### Settings

When running the program for the first time, `example.settings.json` will be copied to `settings.json`. The command below sets video and client ID, however, they are both optional parameters when running the script.
```bash
python app.py <video_id> <client_id>
```

### Notes

- A client ID is currently not required by Twitch. If they eventually decides to require a client ID, `require_client_id` in `settings.json` should be set to `true` to require a client ID when running the script.
- Empty messages means the user has been timed out. There's no known way to get these messages.
- This script is using Twitch's undocumented ReChat API. The script may break at any time.
- The longer VOD, the more API calls are made to Twitch (possibly thousands). Use with care and stay up to date on any rate limits.