import aiotask_context as context
from sanic.response import text

from auth import check_token


async def auth_middleware(request):
    is_authenticated = check_token(request)

    if not is_authenticated:
        return text('You are unauthorized.', 401)


async def set_request_id_middleware(request):
    request_id = request.headers.get('x-request-id')
    context.set('X-Request-ID', request_id)
