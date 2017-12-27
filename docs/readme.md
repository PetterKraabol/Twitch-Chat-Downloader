# Documentation

For more detailed information, please see the [wiki](https://github.com/PetterKraabol/Twitch-Chat-Downloader/wiki).

### Settings

Settings for Twitch Chat Downloader is found in `settings.json`, a file generated after running the program once or by manually copying `settings.example.json`. Use this file to customize your output and add custom formats.

### Arguments

| Argument        | Description                           |
| --------------- | ------------------------------------- |
| `-h` `--help`   | List all commands with descriptions   |
| `-v` `--video`  | Video ID                              |
| `--client-id`   | Twitch client ID                      |
| `-o` `--output` | Output directory. Default: `./output` |
| `-f` `--format` | Output format. Default: `default`     |
| `-q` `--quiet`  | Suppress console output               |
| `--timezone`    | Timezone name                         |

All arguments are optional.

Note that `--output` does not override the format's output directory, but simply prepends its value to the format's directory.

It is not necessary to specify `--client-id` if it has been set in the settings file.

For `--timezone`, see this [Stack Overflow answer](https://stackoverflow.com/a/13867319) to get a list of timezones.

### Formats

Chat messages can be downloaded as subtitles and other custom formats.

| Formats           | Description                             |
| ----------------- | --------------------------------------- |
| `default`         | Custom format example                   |
| `irc`             | IRC chat format                         |
| `srt` `ssa` `ass` | Subtitle formats                        |
| `json`            | Raw JSON data of video and and messages |

### Example usage

```bash
python app.py -v 125936523 --format irc
```

### Notes

* Twitch Chat Downloader uses Twitch API v5, which is to be removed in 2019. Example responses from the Twitch API for video and comments are found in `docs/examples`.
* The Twitch API refers to Twitch messages as "comments", hence, the code does also refer to messages as comments.
