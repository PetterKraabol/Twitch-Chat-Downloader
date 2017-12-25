import twitch
import formats
import os


def download(video_id: str, format_name: str) -> str:
    lines, output = formats.use(format_name, twitch.Video(video_id))

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output, 'w+', encoding='utf-8') as file:
        for line in lines:
            print(line)
            file.write('{}\n'.format(line))

    return output
