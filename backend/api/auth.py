import json
import jwt
import os
from api.players import get_player_by_name
from util import http_response, bad_request, unauthorized, not_found

def generatePolicy(player_id, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = player_id 
 
    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }
 
        authResponse['policyDocument'] = policyDocument
 
    return authResponse

def authenticate(event, contex):
    if not event['body']:
        return bad_request()

    body = json.loads(event['body'])

    username = body['username']
    password = body['password']

    if username is None:
        return bad_request("Missing username")

    if password is None:
        return bad_request("Missing password")

    player = get_player_by_name(username)

    if player is None:
        return not_found()

    if player.check_password(password):
        token = jwt.encode({'player_id': player.player_id}, os.environ.get('SECRET'), algorithm='HS256')
        return http_response({'token': token.decode()})
    else:
        return unauthorized("Wrong password")

def authorize(event, context):
    try:
        bearer, x, token = event['authorizationToken'].partition(' ')
        if not (bearer.lower() == 'bearer'):
            print(f'{ bearer.lower() = } is not { bearer = }')
            return generatePolicy(None, 'Deny', event['methodArn'])

        payload = jwt.decode(token, os.environ.get('SECRET'), algorithms=['HS256'])
 
        player_id = payload['player_id']
 
    except ValueError as err:
        print(err)
        return generatePolicy(None, 'Deny', event['methodArn'])

    except jwt.DecodeError as err:
        print(err)
        return generatePolicy(None, 'Deny', event['methodArn'])

    except Exception as err:
        print(err)
        return generatePolicy(None, 'Deny', event['methodArn'])
 
    return generatePolicy(player_id, 'Allow', event['methodArn'])