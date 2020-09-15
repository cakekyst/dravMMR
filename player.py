from collections import deque
from datetime import datetime
from math import ceil, floor, sqrt


class Player:
    def __init__(self, rscID, name, playlists, seasons, links):
        self.rscID = rscID
        self.name = name
        self.links = links
        self.mmrs = {}
        self.playlists = playlists
        self.seasons = seasons
        for link in links:
            if link != '':
                linkDict = {}
                for season in seasons:
                    seasonDict = {}
                    linkDict[season] = seasonDict
                self.mmrs[link] = linkDict


class MMR:
    def __init__(self, mmr, date='', games=-1):
        self.mmr = mmr
        self.date = date
        self.games = games

    def __repr__(self):
        return f'{self.date} - {self.mmr:>4} - {self.games:>4}'
