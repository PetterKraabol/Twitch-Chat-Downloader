import twitch
import formats
import os
import json
import app.cli


def download(video_id: str, format_name: str) -> str:
    lines, output = formats.use(format_name, twitch.Video(video_id))

    # Create directory
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    # Save to file
    with open(output, 'w+', encoding='utf-8') as file:
        for line in lines:
            if format_name == 'json':
                json.dump(line, file, indent=4, sort_keys=True)
            else:
                if not app.cli.arguments.quiet:
                    print(line)
                file.write('{}\n'.format(line))

    print('\nDownload complete! Output has been saved to {output}'.format(output=output))

    return output
