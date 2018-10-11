import string


def output(video_metadata: dict, output_format: dict):
    # Valid directory characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # Strip illegal characters from title
    if '{title}' in output_format['format']:
        video_metadata['title'] = ''.join(c for c in video_metadata['title'] if c in valid_chars)
