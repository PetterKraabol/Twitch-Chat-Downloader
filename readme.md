# Twitch Chat Downloader

[![Discord](https://user-images.githubusercontent.com/7288322/34471967-1df7808a-efbb-11e7-9088-ed0b04151291.png)](https://discord.gg/wZJFeXC)

A neat Python script to download chat messages from past broadcasts.

### Requirements

* [Python 3.7 or newer](https://www.python.org/downloads/)
* [A Twitch client ID](https://glass.twitch.tv/console/apps)

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

[Documentation](https://github.com/PetterKraabol/Twitch-Chat-Downloader/wiki)
 • [Twitch Python](https://github.com/PetterKraabol/Twitch-Python)
