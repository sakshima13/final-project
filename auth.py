import json
import os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'dev-csu-ji77.us.auth0.com')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE', 'http://dev-csu-ji77.us.com/api/v3')

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    auth_errors = {
        'bearer_error': 'Authorzation header must start with "Bearer".',
        'token_error': 'Auth token not found',
        'invalid_error': 'Authorization header must be bearer token.'
    }
    if not auth_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Auth header must be present'
        }, 401)
    auth_header_content = auth_header.split(' ')
    if 'Bearer' not in auth_header_content:
        raise AuthError({
            'code': 'invalid_header',
            'description': auth_errors['bearer_error']
        }, 401)
    elif len(auth_header_content) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': auth_errors['token_error']
        }, 401)
    elif len(auth_header_content) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': auth_errors['invalid_error']
        }, 401)
    return auth_header_content[1]

def check_permissions(permission, payload):
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not available'
        }, 401)
    return True

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token=token,
                key=rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
@requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)

            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator