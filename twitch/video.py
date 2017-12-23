import twitch.api


class Video:

    def __init__(self, video_id: str):
        self.metadata = twitch.api.video(video_id)
        self.comments = twitch.api.comments(video_id)

    def __str__(self):
        return self.metadata['title']

    def __eq__(self, other):
        return self.id() == other.id()

    def id(self) -> str:
        return self.metadata['_id'].strip('v')
