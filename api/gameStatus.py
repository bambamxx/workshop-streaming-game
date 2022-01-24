"""
    gameStatus.py

        A persistence layer for the game
"""

# a temporary in-memory (not scalable) implementation
# just for testing (will become a partition on Astra)
playerCache = {}
"""
    gameID -> playerID ->
        (gameID, playerID, active, x, y, h, generation, name)
"""

from messaging import makePositionUpdate


def _showCache(title):
    print('PLAYER CACHE DUMP')
    for gid, gvals in sorted(playerCache.items()):
        print('    gameID = %s' % gid)
        for plk, plv in sorted(gvals.items()):
            print('        player %s: %s at %s,%s' % (
                plv[7],
                'ACTIV' if plv[2] else 'inact',
                plv[3],
                plv[4],
            ))


def ensureGameID(gameID):
    playerCache[gameID] = playerCache.get(gameID, {})


def _messageToRow(gameID, active, updateMsg):
    return [
        gameID,
        updateMsg['playerID'],
        active,
        updateMsg['payload']['x'],
        updateMsg['payload']['y'],
        updateMsg['payload']['h'],
        updateMsg['payload']['generation'],
        updateMsg['payload']['name'],
    ]


def _rowToMessage(row):
    return makePositionUpdate(
        row[1],
        row[7],
        row[3],
        row[4],
        row[5],
        row[6],
    )

def storeGameInactivePlayer(gameID, playerID):
    if playerID in playerCache[gameID]:
        playerCache[gameID][playerID][2] = False
    _showCache('store')

def storeGamePlayerStatus(gameID, playerUpdate):
    ensureGameID(gameID)
    #
    pLoad = playerUpdate['payload']
    playerID = playerUpdate['playerID']
    # we can trust x,y etc not to be null at this point
    playerCache[gameID][playerID] = _messageToRow(gameID, True, playerUpdate)
    #
    _showCache('store')


def retrieveGamePlayerStatuses(gameID, excludedIDs = set()):
    # active players only
    ensureGameID(gameID)
    #
    return (
        _rowToMessage(s)
        for s in playerCache[gameID].values()
        if s[2]
        if s[1] not in excludedIDs
    )
    _showCache('retrieve')


def retrieveGamePlayerStatus(gameID, playerID):
    ensureGameID(gameID)
    #
    playerRow = playerCache[gameID].get(playerID)
    if playerRow is not None:
        return _rowToMessage(playerRow)
    else:
        return None