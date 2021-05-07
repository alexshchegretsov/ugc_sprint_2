import datetime as dt

import pymongo
from bson import ObjectId, json_util
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, text

movie_reviews_bp = Blueprint(name='movie reviews')

DEFAULT_PERIOD = 30
DEFAULT_PER_PAGE = 100
DEFAULT_PAGE = 1


@movie_reviews_bp.route('/users/<user_id:string>/movies/<movie_id:string>/reviews', methods=['POST'])
async def create_review(request: Request, user_id: str, movie_id: str):
    data = request.json
    await request.app.mongo.movieMarks.update_one(
        {'movie_id': movie_id, 'user_id': user_id},
        {'$set': {'mark': data['mark']}},
        upsert=True,
    )
    doc = {
        'text': data['text'],
        'user_id': user_id,
        'movie_id': movie_id,
        'mark': data['mark'],
        'created_at': dt.datetime.utcnow().timestamp()
    }
    await request.app.mongo.reviews.insert_one(document=doc)
    return text('Accepted', 202)


@movie_reviews_bp.route('/reviews/sort/date', methods=['GET'])
async def movie_reviews_list_by_date(request: Request):
    period = request.args.get('period', DEFAULT_PERIOD)
    per_page = request.args.get('per_page', DEFAULT_PER_PAGE)
    page = request.args.get('page', DEFAULT_PAGE)

    docs = []
    page = (page - 1) if (page - 1) > 0 else 0
    delta = (dt.datetime.utcnow() - dt.timedelta(days=period)).timestamp()
    cursor = request.app.mongo.reviews.find({'created_at': {'$gt': delta}}) \
        .sort([('created_at', pymongo.DESCENDING)]) \
        .skip(page * per_page) \
        .limit(per_page)

    async for doc in cursor:
        docs.append(doc)

    return json(body=docs, dumps=json_util.dumps)


@movie_reviews_bp.route('/reviews/sort/rating', methods=['GET'])
async def movie_reviews_list_by_rating(request: Request):
    period = request.args.get('period', DEFAULT_PERIOD)
    per_page = request.args.get('per_page', DEFAULT_PER_PAGE)
    page = request.args.get('page', DEFAULT_PAGE)

    docs = []
    page = (page - 1) if (page - 1) > 0 else 0
    delta = (dt.datetime.utcnow() - dt.timedelta(days=period)).timestamp()

    pipeline = [
        {'$match': {'created_at': {'$gt': delta}}},
        {'$group': {'_id': '$review_id', 'rating': {'$avg': '$mark'}}},
    ]
    top_reviews_cursor = request.app.mongo.reviewMarks.aggregate(pipeline)
    obj_to_rating = {ObjectId(x['_id']): x['rating'] for x in await top_reviews_cursor.to_list(None)}

    cursor = request.app.mongo.reviews.find({'_id': {'$in': [*obj_to_rating.keys()]}}) \
        .skip(page * per_page) \
        .limit(per_page)

    async for doc in cursor:
        doc['rating'] = obj_to_rating[doc['_id']]
        docs.append(doc)

    return json(body=sorted(docs, key=lambda x: x['rating'], reverse=True), dumps=json_util.dumps)


@movie_reviews_bp.route('/users/<user_id:string>/movies/<movie_id:string>/reviews/<review_id:string>/mark/<mark:int>',
                        methods=['POST'])
async def review_mark(request: Request, movie_id: str, user_id: str, review_id: str, mark: int):
    doc = await request.app.mongo.reviewMarks.find_one({'_id': ObjectId(review_id)})
    if doc is not None:
        return text('Bad request', 403)

    await request.app.mongo.reviewMarks.insert_one({'user_id': user_id,
                                                    'movie_id': movie_id,
                                                    'review_id': ObjectId(review_id),
                                                    'mark': mark
                                                    })

    return text('Accepted', 202)
