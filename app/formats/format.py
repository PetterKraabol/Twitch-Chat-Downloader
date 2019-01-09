import twitch


class Format:

    def __init__(self, video: twitch.helix.Video, format_dictionary: dict):
        self.video = video
        self.format_dictionary: dict = format_dictionary
