import logging

import aiotask_context as context


def create_key(user_id, movie_id) -> bytes:
    return bytes(f'{user_id}+{movie_id}'.encode())


class RequestIdFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = context.get('X-Request-ID', 'undefined')
        return True
