import json


def serializer(value):
    return json.dumps(value).encode()
