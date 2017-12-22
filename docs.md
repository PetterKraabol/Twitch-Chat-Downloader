# Documentation

## Example

``` bash

python app.py -v 125936523 --start 15 --stop 120 --format relative --cooldown 1

```

## Settings

`settings.json`

| Option | Value | Description |
| ------ | ------ | ----------- |
| require_client_id | *Boolean* | Whether or not to require Twitch client-id |
| client_id | *String* | Twitch client-id |
| output | *String* | Output folder |
| format | *String* | Message format. Available options: `timestamp` `relative` `srt` `ssa` `ass` `raw` |
| print | *Boolean* | `true` displays messages as they are downloaded. `false` displays download progress. |

### Arguments

*Override existing settings* 

| Argument | Description |
| -------- | ----------- |
| `-h` `--help` | List all commands with descriptions |
| `-v` `--video` | Video id |
| `-i` `--client-id` | Twtich client-id |
| `-p` `--print` | Print messages |
| `-o` `--output` | Output folder name |
| `-f` `--format` | Message format |
| `--cooldown` | Cooldown time between api requests in seconds |
| `--start` | Start time in seconds from video start |
| `--stop` | Stop time in seconds from video start |
| `--subtitle-duration` | If using a subtitle format, subtitle duration in seconds |

### Formats

| Formats | Description |
| ------- | ----------- |
| `timestamp` | Message timestamp on your timezone. |
| `relative` | Message timestamp is the time from the start of the video or time specified by the --start argument |
| `srt` `ssa` `ass` | subtitle formats
| `raw` | json array of messages |


### Versions

The settings version number is to make sure your `settings.json` can be properly read by the script. Your version number is compared with with `example.settings.json` which is more likely to be up to date.

If your settings is outdated, compare it with `example.settings.json` to make sure they have the same structure and version number.