import twitch
import twitch.helix as helix

from app.settings import Settings

class Video:

    def __init__(self):
        client_id = Settings().config.get('client_id')
        self.helix: twitch.Helix(client_id, use_cache=True)
