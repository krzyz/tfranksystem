from trueskill import Rating
from api.models import Player
import json
import io
import cgi

def create(event, context):
    rating = Rating()

    print(event)
    print(event['body'])

    fp = io.BytesIO(event['body'].encode('utf-8'))
    pdict = cgi.parse_header(event['headers']['Content-Type'])[1]
    if 'boundary' in pdict:
        pdict['boundary'] = pdict['boundary'].encode('utf-8')
    pdict['CONTENT-LENGTH'] = len(event['body'])
    form_data = cgi.parse_multipart(fp, pdict)
    print('form_data=', form_data)

    player = Player(
        name='Test',
        password='test',
        rank=rating.mu,
        sigma=rating.sigma
    )

    player.save()

    response = {
        "statusCode": 201,
        "headers": {},
        "body": json.dumps(dict(player))
    }

    return response



def getall(event, context):
    players = [dict(x) for x in Player.scan()]

    players_without_passwords = [{k: v for k, v in player.items() if k != 'password'} for player in players]

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