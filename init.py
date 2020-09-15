from csv import reader, writer
from player import MMR, Player
import mmrPuller as puller
import asyncio
import fileManager as fm
from perfMonitor import perfMonitor

if(__name__ == '__main__'):

    monitor = perfMonitor()

    playlists = ['Ranked Duel 1v1',
                 'Ranked Doubles 2v2',
                 'Ranked Solo Standard 3v3',
                 'Ranked Standard 3v3']

    seasons = [11,
               12,
               13,
               14]

    loadProc = monitor.startProc("Load Players")
    players = fm.loadPlayers(playlists, seasons)
    monitor.endProc(loadProc)

    pullProc = monitor.startProc("Pull MMR")
    mmrPuller = puller.mmrPuller()
    asyncio.get_event_loop().run_until_complete(mmrPuller.pullMMRs(players))
    monitor.endProc(pullProc)

    writeProc = monitor.startProc("Write Data")
    fm.writeData(players, playlists, seasons)
    monitor.endProc(writeProc)

    monitor.exit()
