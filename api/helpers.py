import logging

from sanic.request import Request


def create_key(user_id, movie_id) -> bytes:
    return bytes(f'{user_id}+{movie_id}'.encode())


class RequestIdFilter(logging.Filter):

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = Request.id
        return True
