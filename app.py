#!/usr/bin/env python3
import app
import twitch
import formats
import os


def main():

    lines, output = formats.use(app.arguments.format, twitch.Video(app.arguments.video))

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output, 'w+') as file:
        for line in lines:
            print(line)
            file.write('{}\n'.format(line.encode('utf-8')))


if __name__ == "__main__":
    main()
