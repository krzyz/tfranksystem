from trueskill import Rating
from api.models import Player
from util import http_response, bad_request
import json
import io
import cgi

def get_players_by_ids(player_ids):
    players = Player.batch_get(player_ids)

    players_by_ids = {player.player_id: player for player in players}

    return players_by_ids

def create(event, context):
    rating = Rating()

    if event['body']:
        body = json.loads(event['body'])

        player = Player(
            name=body['name'],
            password=body['password'],
            rank=rating.mu,
            sigma=rating.sigma
        )

        player.save()

        return http_response(dict(player), 201)
    return bad_request()



def getall(event, context):
    players = [dict(x) for x in Player.scan()]

    players_without_passwords = [{k: v for k, v in player.items() if k != 'password'} for player in players]

    return http_response({'players': players_without_passwords})

def getone(event, context):
    pass