from twitch.helix import Video

from tcd.settings import Settings


class Format:

    def __init__(self, video: Video, format_name: str):
        self.video: Video = video
        self.format_name: str = format_name
        self.format_dictionary: dict = Settings().config['formats'][format_name]
