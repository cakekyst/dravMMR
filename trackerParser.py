from datetime import date
from player import Mmr, Player
import json


class Parser():
    def __init__(self):
        self.date = date.today().strftime('%m/%d/%y')
        self.player = None

    def feed(self, jsonRAW):
        try:
            data = json.loads(jsonRAW)['data']
            for segment in data['segments']:
                if(segment['type'] == 'playlist'):
                    mmr = Mmr(segment['stats']['rating']['value'], self.date)
                    playlist = segment['metadata']['name']
                    if playlist in self.player.playlists:
                        if(playlist == 'Un-Ranked'):
                            self.player.mmrs[playlist].appendleft(mmr)
                        else:
                            mmr.games = segment['stats']['matchesPlayed']['value']
                            self.player.mmrs[playlist].appendleft(mmr)
        except Exception as e:
            # generic exception handler
            self.player.dataError = True
