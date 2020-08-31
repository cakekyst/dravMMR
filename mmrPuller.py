from player import Player
from trackerParser import Parser
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def pullMMRs(player):
    parser = Parser()
    print(f'Pulling MMRs for {player.name}')
    # The parser instance stores the player to add mmrs from every link
    parser.player = player
    for link in player.links:
        link = formatLink(link)
        parseLink(link, parser)
    print('MMRs pulled.\n')


def formatLink(link):
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
    if 'xbl' in identifier:
        # I don't think this affects non-xbl users, but I exclude them anyway
        identifier = identifier.replace('-', '%20')
    link = baseUrl + identifier
    return link


def parseLink(link, parser):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'}
    # http GET request
    jsonRAW = httpGET(link, headers, 0)
    if jsonRAW != '404' and jsonRAW != 'error':
        parser.feed(jsonRAW)
        if parser.player.dataError:
            # Need to investigate
            print(f'Parse error: {link}')
    else:
        # Usually malformed link
        # Potentially server error
        print(f'HTTP error: {link}')


def httpGET(link, headers, depth):
    # EXTREMELY basic http GET request function
    request = Request(link, headers=headers)
    try:
        data = urlopen(request).read()
        return data.decode('utf8').replace("'", '"')
    except HTTPError as e:
        # Basic catch for all HTPPErrors
        print(f'{e} | {request.get_full_url()}')
        if e.code == 404:
            # Usually caused by a bad link
            return '404'
        elif depth < 3:
            # Usually occurs with a timeout or internal server error
            # Limiting depth to prevent call stack overflow
            return httpGET(request, depth + 1)
        else:
            # This is unexpected behavior, but handled regardless
            return 'error'
