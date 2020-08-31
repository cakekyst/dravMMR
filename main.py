import mmrPuller
import player

if __name__ == "__main__":

    links = ['https://rocketleague.tracker.network/profile/steam/76561198079435423',
             'https://rocketleague.tracker.network/profile/steam/76561198188491262',
             'https://rocketleague.tracker.network/profile/steam/76561198211912808']

    playlists = ['Ranked Duel 1v1',
                 'Ranked Doubles 2v2',
                 'Ranked Solo Standard 3v3',
                 'Ranked Standard 3v3']

    player = player.Player('aiTan', links, playlists)
    mmrPuller.pullMMRs(player)
    for playlist in player.mmrs:
        print(f'{playlist}:')
        for mmr in player.mmrs[playlist]:
            print(mmr)