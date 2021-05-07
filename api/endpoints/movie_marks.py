import datetime as dt

from bson import ObjectId
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, text

movie_marks_bp = Blueprint(name='movie marks', url_prefix='/')


@movie_marks_bp.route('/users/<user_id:string>/movies/<movie_id:string>/mark/<mark:int>', methods=['POST'])
async def create_mark(request: Request, user_id: str, movie_id: str, mark: int):
    doc = await request.app.mongo.movieMarks.find_one({'user_id': user_id, 'movie_id': movie_id})
    if doc is not None:
        return text('Bad request', 403)

    await request.app.mongo.movieMarks.insert_one({
        'user_id': user_id,
        'movie_id': movie_id,
        'mark': mark,
        'created_at': dt.datetime.utcnow().timestamp()
    })
    return text('Accepted', 202)


@movie_marks_bp.route('/users/<user_id:string>/marks/<mark_id:string>/<mark:int>', methods=['PUT'])
async def edit_mark(request: Request, user_id: str, mark_id: str, mark: int):
    old_document = await request.app.mongo.movieMarks.find_one({'user_id': user_id, '_id': ObjectId(mark_id)})
    if not old_document:
        return text('Bad request', 403)

    await request.app.mongo.movieMarks.update_one({'_id': ObjectId(mark_id)}, {'$set': {'mark': mark}})
    return text('Accepted', 202)


@movie_marks_bp.route('/users/<user_id:string>/marks/<mark_id:string>', methods=['DELETE'])
async def delete_mark(request: Request, user_id: str, mark_id: str):
    await request.app.mongo.movieMarks.find_one({'user_id': user_id, '_id': ObjectId(mark_id)})
    return text('Accepted', 202)


@movie_marks_bp.route('/movies/<movie_id:string>/likes', methods=['GET'])
async def movie_likes(request: Request, movie_id: str):
    res = await request.app.mongo.movieMarks.count_documents({'movie_id': movie_id, 'mark': {'$eq': 10}})
    return json({'data': res}, 200)


@movie_marks_bp.route('/movies/<movie_id:string>/dislikes', methods=['GET'])
async def movie_dislikes(request: Request, movie_id: str):
    res = await request.app.mongo.movieMarks.count_documents({'movie_id': movie_id, 'mark': {'$eq': 0}})
    return json({'data': res}, 200)


@movie_marks_bp.route('/movies/<movie_id:string>/rating', methods=['GET'])
async def movie_rating(request: Request, movie_id: str):
    marks = []

    async for doc in request.app.mongo.movieMarks.find({'movie_id': movie_id}):
        mark = doc['mark']
        marks.append(mark)

    avg_rating = sum(marks) // len(marks)
    return json({'data': avg_rating}, 200)
