# Documentation

It is highly recommended to look at `settings.json`, a file that is automatically generated after running the script once.

- [Arguments](arguments.md)
- [Formats](formats.md)

### Example usage

```bash
python app.py -v 125936523 --format irc
```

### Notes
- Twitch Chat Downloader uses Twitch API v5, which is to be removed in 2019.
- The Twitch API refers to Twitch messages as "comments", hence, the code does also refer to messages as comments.