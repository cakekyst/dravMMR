from datetime import date
from player import MMR, Player
import json


class Parser():
    def __init__(self):
        self.date = date.today().strftime('%m/%d/%y')

    def feed(self, jsonRAW, link):
        try:
            data = json.loads(jsonRAW)['data']
            for segment in data:
                if(segment['metadata']['name'] in self.player.playlists):
                    mmr = MMR(segment['stats']['rating']['value'], self.date, link)
                    playlist = segment['metadata']['name']
                    season = segment['attributes']['season']
                    if(playlist != 'Un-Ranked'):
                        mmr.games = segment['stats']['matchesPlayed']['value']
                    self.player.mmrs[link][season][playlist] = mmr
            return False
        except Exception as e:
            return True
