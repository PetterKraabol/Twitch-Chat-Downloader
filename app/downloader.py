import twitch
import formats
import os
import json
import app.cli
import sys


def draw_progress(current: float, end: float):
    sys.stdout.write('Progress: {}%\r'.format('%.2f' % (current * 10 / end * 10)))
    sys.stdout.flush()


def download(video_id: str, format_name: str) -> str:
    video: twitch.Video = twitch.Video(video_id)
    lines, output = formats.use(format_name, video)

    # Create directory
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    # Save to file
    with open(output, 'w+', encoding='utf-8') as file:
        for line, line_dictionary in lines:
            if format_name == 'json':
                json.dump(line, file, indent=4, sort_keys=True)
            else:
                if not app.cli.arguments.quiet:
                    if app.cli.arguments.preview:
                        print(line)
                    elif 'content_offset_seconds' in line_dictionary:
                        draw_progress(line_dictionary['content_offset_seconds'], video.metadata['length'])
                file.write('{}\n'.format(line))

    return output
