from trueskill import Rating, rate
from api.models import Player, PlayerMap, TeamMap, Match, HistoricalRank
from api.players import get_players_by_ids
from util import http_response, bad_request, authorize, not_found
from collections import ChainMap
from dateutil import parser
from datetime import datetime, timedelta, timezone
from api.exceptions import NotFoundException, MissingReferenceException, MatchNotTheMostRecentException
from pynamodb.connection import Connection
from pynamodb.transactions import TransactWrite
import json
import os

region = os.environ.get('REGION')

def remove(match_id):
    match = next(Match.query(match_id), None)
    if match is None:
        raise NotFoundException

    player_ids = []
    for team in match.teams:
        for player in team.players:
            player_ids.append(player.player_id)

    connection = Connection(region=region)

    with TransactWrite(connection=connection) as transaction:
        for player_id in player_ids:
            player = next(Player.query(player_id), None)
            if player is None:
                raise MissingReferenceException
            ranks = list(HistoricalRank.query(player_id, scan_index_forward=False, limit=2))
            if len(ranks) < 1:
                raise MissingReferenceException
            if len(ranks) == 1:
                previous_rank = Rating()
            else:
                previous_rank = Rating(mu=ranks[1].rank, sigma=ranks[1].sigma)

            new_rank = ranks[0]

            if new_rank.match_id != match_id:
                raise MatchNotTheMostRecentException

            transaction.update(player, actions=[
                Player.rank.set(previous_rank.mu),
                Player.sigma.set(previous_rank.sigma),
            ])

            transaction.delete(new_rank)

        transaction.delete(match)
        

def remove_handler(event, contex):
    authorize(event)

    try:
        match_id = event['pathParameters']['match_id']
    except Exception as e:
        return bad_request(str(e))
    try:
        remove(match_id)
    except NotFoundException:
        return not_found()
    except MissingReferenceException:
        return bad_request('Database in inconsistent state')
    except MatchNotTheMostRecentException:
        return bad_request('Match is not the most recent for players')
    
    return http_response(None, 204)

def create(event, contex):
    authorize(event)

    if event['body']:
        try: 
            body = json.loads(event['body'])

            teams = body['teams']
            ranks = body['ranks']
            match_time = parser.parse(body['date'])
        except Exception as e:
            return bad_request(str(e))


        if match_time > (datetime.now(tz=timezone.utc)):
            return bad_request('Date is in the future!')
        
        matches = [match.datetime for match in Match.scan()]
        if len(matches) > 0:
            matches.sort()
            last_match_time = matches[-1]

            if last_match_time > match_time:
                return bad_request("Later match already in the database!")

        player_ids = [player_id for players in teams for player_id in players]

        players_by_id = get_players_by_ids(player_ids)

        teams_with_names = [TeamMap(players=[PlayerMap(player_id=player_id, name=players_by_id[player_id].name) for player_id in players]) for players in teams]

        match = Match(teams=teams_with_names, ranks=ranks, datetime=match_time)

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
    matches = [match.to_dict() for match in Match.scan()]

    return http_response({'matches': matches})