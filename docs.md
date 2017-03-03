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
| format | *String* | Message format. Available options: `timestamp` `relative` `srt` `ssa` `ass` |
| print | *Boolean* | `true` displays messages as they are downloaded. `false` displays download progress. |

## Arguments

*Override existing settings* 

| Argument | Description |
| -------- | ----------- |
| `-h` `--help` | List all commands with descriptions |
| `-v` `--video` | Video id |
| `-i` `--client-id` | Twtich client-id |
| `-p` `--print` | Print messages |
| `-o` `--output` | Output folder name |
| `-f` `--format` | Message format |
| `--cooldown` | Cooldown time between API requests in seconds |
| `--start` | Start time in seconds from video start |
| `--stop` | Stop time in seconds from video start |

## Formats

| Formats | Description |
| ------- | ----------- |
| `timestamp` | shows the time on your timezone. |
| `relative` | shows the time from the start of the video |
| `srt` `ssa` `ass` | subtitle formats
