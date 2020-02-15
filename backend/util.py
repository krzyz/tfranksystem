import json

def http_response(body, status_code = 200):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json', 
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': json.dumps(body)
    }

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
    print(event['requestContext']['authorizer'])
    if 'principalId' not in event['requestContext']['authorizer']:
        return forbidden()
    if event['requestContext']['authorizer']['principalId'] is None:
        return forbidden()