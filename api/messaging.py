"""
    messaging.py
"""

from uuid import uuid4

from utils import dictMerge


def validatePosition(updDict, halfX, halfY):
    """
    Utility function to keep the 'x' and 'y' in a dict
    bound within the game field, respecting null values and other keys
    that may be present in the dict expressing the item position.
    """
    def _constrainNoneAware(val, minv, maxv):
        if val is None:
            return val
        else:
            return max(minv, min(val, maxv))

    payload = {
        'x': _constrainNoneAware(updDict['payload']['x'], 0, 2*halfX - 2),
        'y': _constrainNoneAware(updDict['payload']['y'], 0, 2*halfY - 2),
    }
    return dictMerge(
        {
            'payload': payload,
        },
        default=updDict,
    )


def makePositionUpdate(client_id, client_name, x, y, h, generation):
    return {
        'messageType': 'player',
        'playerID': client_id,
        'payload': {
            'x': x,
            'y': y,
            'h': h,
            'generation': generation,
            'name': client_name,
        },
    }    


def makeEnteringPositionUpdate(client_id, client_name, halfX, halfY):
    return makePositionUpdate(client_id, client_name, halfX-1, halfY-1,
                              False, 0)


def makeLeavingUpdate(client_id):
    """
    A default 'leaving' message to publish to the Pulsar topic
    in case a client disconnection is detected
    """
    return {
        'messageType': 'leaving',
        'playerID': client_id,
        'payload': {
            'name': '',
        },
    }


def makeWelcomeUpdate(client_id):
    """
    A server-generated chat message to greet a new player
    """
    return {
        'messageType': 'chat',
        'payload': {
            'id': str(uuid4()),
            'name': '** API **',
            'text': 'Welcome to the game!',
        },
        'playerID': '_api_server_',
    }


def makeGeometryUpdate(hsX, hsY):
    """
    Prepare a message containing the field geometry info
    """
    return {
        'messageType': 'geometry',
        'payload': {
            'halfSizeX': hsX,
            'halfSizeY': hsY,
        },
    }
