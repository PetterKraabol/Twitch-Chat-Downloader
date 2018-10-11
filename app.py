#!/usr/bin/env python3
from typing import List

import app


def main():
    if app.arguments.format == 'all':

        # Whitelist and blacklist
        whitelist: List[str] = []
        blacklist: List[str] = []

        # Populate lists if configured in settings
        if 'all' in app.settings['formats']:
            if 'whitelist' in app.settings['formats']['all']:
                whitelist = app.settings['formats']['all']['whitelist']

            if 'blacklist' in app.settings['formats']['all']:
                blacklist = app.settings['formats']['all']['blacklist']

        # If not input, download JSON data form API and
        # use it as input value for the other formats.
        if app.arguments.input is None:
            app.arguments.input = app.download(app.arguments.video, 'json')

        # Download all formats. Ignore 'all' and 'json'.
        for format_name in app.settings['formats']:
            if format_name not in ['all', 'json']:

                if (whitelist and format_name not in whitelist) or (blacklist and format_name in blacklist):
                    if app.arguments.verbose:
                        print('Skipping {format_name}'.format(format_name=format_name))
                    continue
                else:
                    app.download(app.arguments.video, format_name)

    else:
        app.download(app.arguments.video, app.arguments.format)

    if app.arguments.verbose:
        print('Done')


if __name__ == "__main__":
    main()
