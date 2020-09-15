from csv import reader
from datetime import datetime
import fileManager as fm
from player import Player
from random import uniform
from time import sleep
from trackerParser import Parser
import asyncio
import aiohttp
import sys


class mmrPuller:
    def __init__(self):
        self.previous = 0
        self.done = 0
        self.links = 0
        self.failed = 0
        self.failedLinks = []
        self.tasks = []
        self.start = datetime.now()

    async def pullMMRs(self, players):
        self.total = len(players)
        done = set()
        tasks = set()
        async with aiohttp.ClientSession() as client:
            print('Pulling MMRs for {0} player(s)...'.format(self.total))
            for player in players:
                while(len(tasks) > 49):
                    done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                tasks.add(asyncio.create_task(
                    self.parseRequest(client, player)))
            while(len(tasks) > 0):
                done, tasks = await asyncio.wait(tasks)
            fm.writeFailedLinks(self.failedLinks, self.failed)
            print('MMRs pulled.\n')

    async def parseRequest(self, client, player):
        parser = Parser()
        parser.player = player
        for link in player.links:
            for season in player.seasons:
                if(link != ''):
                    endpoint = formatLink(link, season)
                    jsonRAW = await httpGET(client, endpoint, 0)
                    parseError = parser.feed(jsonRAW, link)
                    if(parseError):
                        self.failedLinks.append([link, parser.player])
                        self.failed += 1
        self.done += 1
        printProgress(self.start, self.total, self.done, self.failed)


def formatLink(link, season):
    # Temporary link-alteration code
    # Though not best practice, I'm keeping each potential alteration as-is
    # until I am confident I have found most if not all sources of error
    baseUrl = 'https://api.tracker.gg/api/v2/rocket-league/standard/profile/'
    linkStrings = link.split('/profile/')
    identifier = linkStrings[1]
    identifier = identifier.replace('ps/', 'psn/')
    identifier = identifier.replace('ps4/', 'psn/')
    identifier = identifier.replace('xbox/', 'xbl/')
    identifier = identifier.replace('Xbox/', 'xbl/')
    identifier = identifier.replace(' ', '%20')
    identifier = identifier.replace('/overview', '')
    indentifier = identifier.replace('mmr/', '/')
    if 'xbl' in identifier:
        # I don't think this affects non-xbl users, but I exclude them anyway
        identifier = identifier.replace('-', '%20')
    link = baseUrl + identifier
    link += "/segments/playlist?season={0}".format(season)
    return link


async def httpGET(client, link, depth):
    async with client.get(link) as response:
        data = await response.read()
        if response.status == 200:
            jsonRaw = data.decode('utf8')
            return jsonRaw
        elif response.status == 404:
            return "404"
        elif depth < 3:
            return httpGET(client, link, depth + 1)
        else:
            return "error"


def printProgress(start, total, done, failed, previous=0):
    current = datetime.now()
    if(done == 0):
        return
    remaining = (current - start) / (done + previous) * (total - done + failed)
    end = current + remaining
    length = len(str(total))
    toPrint = '\r    {0:>{1}}/{2}'.format(done, length, total)
    toPrint += ' - {0:>5}%'.format(round(done / total * 100, 1))
    toPrint += ' | {0:>{1}}'.format(failed, length)
    toPrint += ' | {0} - {1}'.format(str(remaining)[:7], str(end)[11:19])
    sys.stdout.write(toPrint)
    if(total != done):
        sys.stdout.flush()
    else:
        sys.stdout.write('\n')