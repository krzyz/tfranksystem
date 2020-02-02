from trueskill import Rating, rate
from api.models import Player, PlayerMap, TeamMap, Match, HistoricalRank
from api.players import get_players_by_ids
from util import http_response, bad_request
from collections import ChainMap
import json

def create(event, contex):
    if event['body']:
        body = json.loads(event['body'])

        teams = body['teams']
        ranks = body['ranks']

        player_ids = [player_id for players in teams for player_id in players]

        players_by_id = get_players_by_ids(player_ids)

        teams_with_names = [TeamMap(players=[PlayerMap(player_id=player_id, name=players_by_id[player_id].name) for player_id in players]) for players in teams]

        match = Match(teams=teams_with_names, ranks=ranks)

        team_ratings = []
        for players in teams:
            ratings = {}
            for player_id in players:
                player = players_by_id[player_id]
                ratings.update({player_id: Rating(player.rank, player.sigma)})
            team_ratings.append(ratings)

        new_team_ratings = ChainMap(*rate(team_ratings, ranks))

        match.save()

        for player_id, player in players_by_id.items():
            new_rating = new_team_ratings[player_id]

            historical_rank = HistoricalRank(
                player_id=player_id,
                match_id=match.match_id,
                datetime=match.datetime,
                rank=new_rating.mu,
                sigma=new_rating.sigma,
            )

            historical_rank.save()

            player.update(actions=[
                Player.rank.set(new_rating.mu),
                Player.sigma.set(new_rating.sigma),
            ])

        return http_response(match.to_dict(), 201)
    return bad_request()

def getall(event, context):
    pass