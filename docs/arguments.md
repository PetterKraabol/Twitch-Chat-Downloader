# Arguments

| Argument        | Description                           |
| --------------- | ------------------------------------- |
| `-h` `--help`   | List all commands with descriptions   |
| `-v` `--video`  | Video id                              |
| `--client-id`   | Twitch client ID                      |
| `-o` `--output` | Output directory. Default: `./output` |
| `-f` `--format` | Output format. Default: `irc`         |

Note that `--output` does not override the format's output directory, but simply prepends its value to the format's directory.

It is not necessary to specify `--client-id` if it has been set in the settings file.
