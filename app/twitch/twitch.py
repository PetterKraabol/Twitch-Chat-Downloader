import twitch
import twitch.helix as helix

from app.singleton import Singleton
from app.settings import Settings


class Twitch(metaclass=Singleton):

    def __init__(self):
        client_id = Settings().config.get('client_id')
        self.helix: twitch.Helix(client_id, use_cache=True)
