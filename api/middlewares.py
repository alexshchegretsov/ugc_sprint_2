from auth import check_token
from sanic import text


async def auth_middleware(request):
    is_authenticated = check_token(request)

    if not is_authenticated:
        return text('You are unauthorized.', 401)
