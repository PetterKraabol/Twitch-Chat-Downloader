# Twitch Chat Downloader

[![Discord](https://user-images.githubusercontent.com/7288322/34471967-1df7808a-efbb-11e7-9088-ed0b04151291.png)](https://discord.gg/wZJFeXC)

`pip install tcd`

A neat tool to download chat messages from past broadcasts.

### Requirements

* [Python 3.7 or newer](https://www.python.org/downloads/)
* [A Twitch client ID](https://glass.twitch.tv/console/apps)

### Usage

```bash
tcd
```

```bash
# Download chat from VODs by video id
tcd --video 789654123,987456321 --format irc --output ~/Downloads
```

```bash
# Download chat from the first 10 VODs from multiple streamers
tcd --channel sodapoppin,nymn,lirik --first=10
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
