from csv import reader, writer
from os import remove, listdir
from os.path import isfile
from player import Player

shorthandDict = {
    'Ranked Duel 1v1': '1s',
    'Ranked Doubles 2v2': '2s',
    'Ranked Solo Standard 3v3': 'solo3s',
    'Ranked Standard 3v3': '3s'
}

inputFolder = "./inputcsv/"
outputFolder = "./outputcsv/"


def writeFailedLinks(failed, numFailed):
    if(numFailed == 0):
        toPrint = '\nNo failed links.'
        if(isfile('failedLinks.csv')):
            remove('failedLinks.csv')
            toPrint += ' Deleted failedLinks.csv.'
        print(toPrint)
    else:
        print('Saving {0} failed link(s)...'.format(numFailed))
        failed.sort(key=lambda link: link[1].rscID)
        with open('failedLinks.csv', 'w', newline='', encoding='utf-8') as failedLinks:
            csvWriter = writer(failedLinks)
            for link in failed:
                csvWriter.writerow([link[1].rscID, link[1].name, link[0]])
        print('{0} failed link(s) saved.'.format(numFailed))


def loadPlayers(playlists, seasons):
    files = listdir(inputFolder)
    if len(files) > 1:
        print('\nOnly 1 input file expected, exiting...')
        exit(1)
    else:
        print('\nLoading links from {0}'.format(files[0]))
    inputFile = inputFolder + files[0]
    players = []
    try:
        with open(inputFile, 'r', newline='', encoding='windows-1252') as savedData:
            csvReader = reader(savedData, delimiter=',')
            for line in csvReader:
                if(line[0] == 'RSC Unique ID'):
                    continue
                player = Player(line[0], line[1], playlists, seasons, line[2:])
                players.append(player)
        print('Links loaded.\n')
    except FileNotFoundError:
        print('Link file not found.\n')
    return players


def writeData(players, playlists, seasons):
    print('Writing retrieved data...')
    outputFile = outputFolder + 'output.csv'
    with open(outputFile, 'w', encoding='windows-1252', newline='') as pMmr:
        csvWriter = writer(pMmr)
        headerRow = ["RSCID", "Name", "Link"]
        for season in seasons:
            for playlist in playlists:
                headerRow.append(
                    '{0}-{1}'.format(season, shorthandDict[playlist]))
                headerRow.append('GP')
        csvWriter.writerow(headerRow)
        for player in players:
            for link in player.links:
                if link != '':
                    row = [player.rscID, player.name, link]
                    for season in seasons:
                        for playlist in playlists:
                            try:
                                row.append(
                                    player.mmrs[link][season][playlist].mmr)
                                row.append(
                                    player.mmrs[link][season][playlist].games)
                            except KeyError:
                                row.extend([0, 0])
                    csvWriter.writerow(row)
