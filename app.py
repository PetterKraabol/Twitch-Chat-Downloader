#!/usr/bin/env python3
import app


def main():

    if str(app.arguments.format).lower() in ['ass']:
        print('\n{format_name} is not yet implemented.'.format(format_name=str(app.arguments.format).lower()))
        print('Stay updated on https://github.com/PetterKraabol/Twitch-Chat-Downloader')
        exit()

    else:
        app.download(app.arguments.video, app.arguments.format)


if __name__ == "__main__":
    main()
