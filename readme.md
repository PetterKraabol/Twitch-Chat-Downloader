# Twitch Chat Downloader

A neat Python script to download chat messages from past broadcasts.

### Requirements

* [Python 3](https://www.python.org/downloads/)
* [A Twitch client ID](https://dev.twitch.tv/dashboard/apps)

### Installation

```bash
git clone https://github.com/PetterKraabol/Twitch-Chat-Downloader.git
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
python app.py -v 125936523 --format irc --output ~/Downloads
```

### Status

This script has been rewritten for compatibility with the Twitch API and improve performance for long VODs. Some features are yet to be reimplemented.

| Formats           | Status      |
| ----------------- | ----------- |
| Custom formats    | Done        |
| IRC               | In progress |
| JSON              | In progress |
| SRT subtitles     | In progress |
| SSA/ASS subtitles | In progress |
