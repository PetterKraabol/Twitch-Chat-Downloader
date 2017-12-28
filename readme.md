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

### Features
- Create your own [custom formats](https://github.com/PetterKraabol/Twitch-Chat-Downloader/wiki/Custom-formats)
- IRC format with badges
- SRT and SSA [subtitle formats](https://github.com/PetterKraabol/Twitch-Chat-Downloader/wiki/Formats)
- Raw JSON data from the Twitch API
- Timezone conversion

---

[Check out the Wiki](https://github.com/PetterKraabol/Twitch-Chat-Downloader/wiki)
