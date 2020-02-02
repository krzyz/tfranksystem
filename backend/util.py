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
        'message': message
    })