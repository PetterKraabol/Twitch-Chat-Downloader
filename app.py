#!/usr/bin/env python3
import cli
import twitch
import formatter


def main():
    video: twitch.Video = twitch.Video(cli.arguments.video)

    for comment in video.comments:
        print(formatter.use(cli.arguments.format, comment))


if __name__ == "__main__":
    main()
