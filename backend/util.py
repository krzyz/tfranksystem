import json

def http_response(body = None, status_code = 200):
    response = {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
    }

    if body is not None:
        response = dict(response, body=json.dumps(body))

    return response

def bad_request(message='Invalid request'):
    return http_response({
        'message': message,
    }, 400)

def unauthorized(message='Not authorized'):
    return http_response({
        'message': message
    }, 401)

def forbidden(message='Forbidded'):
    return http_response({
        'message': message
    }, 403)

def not_found(message='Not found'):
      return http_response({
        'message': message
    }, 404)

def authorize(event):
    if 'principalId' not in event['requestContext']['authorizer']:
        print(f"no principalId in {event['requestContext']['authorizer']}")
        return forbidden()
    if event['requestContext']['authorizer']['principalId'] is None:
        print(event)
        print(f'principalId is none')
        return forbidden()