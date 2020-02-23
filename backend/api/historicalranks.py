from trueskill import Rating
from util import http_response, group
from api.models import Player, HistoricalRank
import json

def getall():
    ranks = list(HistoricalRank.scan())
    ranks_by_player = group(HistoricalRank.scan(), 'player_id', lambda x: {'time': str(x.datetime), 'rank': x.rank, 'sigma': x.sigma})

    series_by_player = {player_id: {k: [rank[k] for rank in ranks] for k in ranks[0]} for player_id, ranks in ranks_by_player.items()}

    return series_by_player

def getall_handler(event, context):
    ranks = getall()
    return http_response(ranks)

def getone(event, context):
    pass