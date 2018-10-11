import json
import os
import sys

import app.cli
import app.formats as formats
import app.twitch as twitch


def draw_progress(current: float, end: float, description: str = 'Downloading'):
    sys.stdout.write('[{}] {}%\r'.format(description, '%.2f' % min(current * 10 / end * 10, 100.00)))
    sys.stdout.flush()


def download_multiple_formats():
    pass


def download(video_id: str, format_name: str) -> str:
    if app.cli.arguments.verbose:
        print('Downloading {} initialized'.format(format_name))

    # Get Video
    video: twitch.Video = twitch.Video(video_id)

    # Format video comments and output
    lines, output = formats.use(format_name, video)

    # Create output directory
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    # Save to file
    with open(output, 'w+', encoding='utf-8') as file:

        # Special case for saving JSON data
        if format_name == 'json':
            for data in lines:
                json.dump(data, file, indent=4, sort_keys=True)
        else:
            # Save formatted comments/lines to file
            for line, line_dictionary in lines:
                if not app.cli.arguments.quiet and not app.cli.arguments.verbose:
                    if app.cli.arguments.preview:
                        print(line)
                    elif 'content_offset_seconds' in line_dictionary:
                        draw_progress(line_dictionary['content_offset_seconds'], video.metadata['length'], format_name)

                file.write('{}\n'.format(line))

    # Print finished message
    if not app.cli.arguments.quiet:
        if app.cli.arguments.verbose:
            print('Finished downloading {} to {}'.format(format_name, output))
        else:
            print('[{}] {}'.format(format_name, output))
    return output
