# Twitch Chat Downloader

Neat python script to download chat messages from past broadcasts

### Requirements

- [Python 2.7 or 3.4+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [Requests library installation guide](http://docs.python-requests.org/en/master/user/install/)

### Installation

```bash
git clone git@github.com:PetterKraabol/Twitch-Chat-Downloader.git
cd Twitch-Chat-Downloader
pip install -r requirements.txt
```

### Usage

```bash
python app.py
```

```bash
python app.py --help
```

```bash
python app.py -v 125936523 --start 15 --stop 120 --format relative --cooldown 0 --print --output ~/Downloads
```

### Notes

- A client ID is currently not required by Twitch. If they eventually decides to require a client ID, `require_client_id` in `settings.json` should be set to `true`.
- Empty messages means the user has been timed out. There's no known way to get these.
- This script is using Twitch's undocumented ReChat API. it might break at any time.
- Consider increasing the delay between API calls in `settings.json` to avoid a potential temporary block from Twitch for sending too many requests when downloading messages from very long streams.