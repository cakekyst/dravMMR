from collections import deque
from datetime import datetime
from math import ceil, floor, sqrt


class Player:
    def __init__(self, name, links, playlists):
        self.name = name
        self.links = links
        self.playlists = playlists
        self.mmrs = {}
        for playlist in playlists:
            self.mmrs[playlist] = deque()
        self.dataError = False

class Mmr:
    def __init__(self, mmr, date='', games=-1):
        self.mmr = mmr
        self.date = date
        self.games = games

    def __repr__(self):
        return f'{self.date} - {self.mmr:>4} - {self.games:>4}'
