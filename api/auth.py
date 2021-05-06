import jwt
from settings import JWT_ALGORITHM, PUBLIC_KEY


def check_token(request):
    if not request.token:
        return False

    try:
        payload = jwt.decode(request.token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
        setattr(request, 'token_payload', payload)
    except jwt.exceptions.InvalidTokenError:
        return False
    else:
        return True
