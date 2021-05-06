from helpers import create_key
from sanic import Blueprint, Request, text
from settings import USERS_VIEWS_FILMS_TOPIC

event_view_bp = Blueprint(name='views', url_prefix='/views')


@event_view_bp.route('/films', methods=['POST'])
async def view_films(request: Request):
    _data = request.json
    user_id = _data.get('user_id')
    movie_id = _data.get('movie_id')

    data = {
        'offset': _data.get('offset'),
        'event_time': _data.get('event_time'),
        'user_id': user_id,
        'movie_id': movie_id
    }

    # aiokafka natively uses buffer space defined in app setup (max_batch_size).
    # After this amount `send` coroutine will block until batch is drained.
    await request.app.ctx.producer.send(topic=USERS_VIEWS_FILMS_TOPIC, key=create_key(user_id, movie_id), value=data)
    return text('Accepted', 202)
