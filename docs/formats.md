# Formats

Chat messages can be downloaded as subtitles and other custom formats.

| Formats           | Description                                         |
| ----------------- | --------------------------------------------------- |
| `default`         | Custom format example                               |
| `irc`             | IRC chat format                                     |
| `srt` `ssa` `ass` | Subtitle formats                                    |
| `json`            | JSON array of comments directly form the Twitch API |

## Custom Formats

To add your own custom format, simply add a new format in `settings.json`, within `formats: {...}`. You may look at an existing custom format, `default`, and modify it to your needs. Variables are based on JSON responses form the Twitch API, transformed into a python dictionary. Comments use values from comment data, whereas output variables uses video data.

JSON response examples are found in example files within `docs/examples`. Examples to extract these values using format variables are shown below.

Timestamp format is based on Python's [datetime format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior).

### Examples

#### Variables

Variable `{commenter[display_name]}` will output _Zarlach_, given this JSON data:

```JSON
{
    "commenter": {
        "display_name": "Zarlach"
    }
}
```

#### Adding a new custom format

Add the following within `formats` in `settings.json`

```JSON
"myformat": {
    "comments": {
        "format": "{created_at} {commenter[display_name]} Kappa {message[body]}",
        "timestamp": "%X"
    },
    "output": {
        "format": "{channel[name]}/{_id} - {title}.txt",
        "timestamp": "%x"
    }
}
```

##### Output

Comment: `12:00:14 Zarlach: Kappa Hello world`

Output: `lirik/12/22/17/v212237951 - Sewb Sewnday - @LIRIK.txt`

Choosing where the output directory is placed is done with the `--output` argument. For example,`--output ~/Downlaods` will create the file `~/Downlaods/lirik/12/22/17/v212237951 - Sewb Sewnday - @LIRIK.txt`

### Special Formats

Formats such as `irc`, `srt` and `ssa/ass` are special formats that require scripting for proper formatting. If you want to make your own special format, you may look at how these are made within the `formats` folder.
