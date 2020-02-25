import jwt


def create_jwt_token(id):
    payload = {'id': id}
    token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
    return token


# def decode_token(token):
#     payload = jwt.decode(token, 'secret')
#     return payload