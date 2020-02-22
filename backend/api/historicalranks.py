from trueskill import Rating
from api.models import Player, HistoricalRank
import json

def getall(event, context):
    print('getting all')
    players = [dict(x) for x in Player.scan()]

    response = {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({
            "players": players
        })
    }
    return response

def getone(event, context):
    pass