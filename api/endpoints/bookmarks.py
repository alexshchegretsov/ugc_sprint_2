import datetime as dt

from bson import ObjectId
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, text

bookmarks_bp = Blueprint(name='bookmarks')


@bookmarks_bp.route('/users/<user_id:string>/bookmarks/movies/<movie_id:string>', methods=['POST'])
async def create_bookmark(request: Request, user_id: str, movie_id: str):
    await request.app.mongo.bookmarks.insert_one({
        'user_id': user_id,
        'movie_id': movie_id,
        'created_at': dt.datetime.now().timestamp()
    })
    return text('Accepted', 202)


@bookmarks_bp.route('/users/<user_id:string>/bookmarks/<bookmark_id:string>', methods=['DELETE'])
async def delete_bookmark(request: Request, user_id: str, bookmark_id: str):
    await request.app.mongo.bookmarks.delete_one({'_id': ObjectId(bookmark_id), 'user_id': user_id})
    return text('Accepted', 202)


@bookmarks_bp.route('/users/<user_id:string>/bookmarks', methods=['GET'])
async def list_bookmark(request: Request, user_id: str):
    docs = []

    async for doc in request.app.mongo.bookmarks.find({'user_id': user_id}):
        docs.append(doc)

    return json(docs, 200)
