#!/usr/bin/env python3
import app
import twitch
import formats


def main():
    video: twitch.Video = twitch.Video(app.arguments.video)

    for comment in video.comments:
        print(formats.use(app.arguments.format, comment))


if __name__ == "__main__":
    main()
