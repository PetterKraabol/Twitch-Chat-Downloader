import twitch
import formats
import os
import json
import app.cli
import sys


def draw_progress(current: float, end: float):
    sys.stdout.write('Progress: {}%\r'.format('%.2f' % min(current * 10 / end * 10, 100.00)))
    sys.stdout.flush()


def download(video_id: str, format_name: str) -> str:
    if app.cli.arguments.verbose:
        print('Downloading {} initialized'.format(format_name))

    video: twitch.Video = twitch.Video(video_id)
    lines, output = formats.use(format_name, video)

    # Create directory
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    # Save to file
    with open(output, 'w+', encoding='utf-8') as file:

        if format_name == 'json':
            for data in lines:
                json.dump(data, file, indent=4, sort_keys=True)

        for line, line_dictionary in lines:
            if not app.cli.arguments.quiet and not app.cli.arguments.verbose:
                if app.cli.arguments.preview:
                    print(line)
                elif 'content_offset_seconds' in line_dictionary:
                    draw_progress(line_dictionary['content_offset_seconds'], video.metadata['length'])

            file.write('{}\n'.format(line))

    if not app.cli.arguments.quiet:
        if app.cli.arguments.verbose:
            print('Finished downloading {} to {}'.format(format_name, output))
        else:
            print(output)
    return output
