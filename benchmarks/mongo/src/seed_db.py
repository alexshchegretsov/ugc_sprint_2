from multiprocessing import Pool

import tqdm
from pymongo import MongoClient

from benchmarks.mongo.src.config import DB_NAME, MONGO_HOST, MONGO_PORT
from benchmarks.mongo.src.test_data_gen import (
    generate_movie_and_related_documents,
    generate_user_documents,
    movie_ids
)


def upload_users_documents():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client.get_database(DB_NAME)

    collection = db.get_collection('users')
    collection.insert_many(generate_user_documents(), ordered=False)


def upload_movie_ratings_and_reviews(movie_id):
    # https://pymongo.readthedocs.io/en/stable/faq.html?highlight=never%20do%20this#using-pymongo-with-multiprocessing
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client.get_database(DB_NAME)

    movie, ratings, reviews = generate_movie_and_related_documents(movie_id)

    movies_coll = db.get_collection('movies')
    movies_coll.insert_one(movie)

    if ratings:
        ratings_coll = db.get_collection('movie_ratings')
        ratings_coll.insert_many(ratings, ordered=False)

    if reviews:
        reviews_coll = db.get_collection('reviews')
        reviews_coll.insert_many(reviews, ordered=False)

    client.close()


if __name__ == '__main__':
    print('Uploading user data to Mongo')
    upload_users_documents()
    print('Done!')

    print('Uploading movies, ratings and reviews data to Mongo')
    with Pool() as pool:
        r = list(tqdm.tqdm(
            pool.imap(upload_movie_ratings_and_reviews, movie_ids),
            total=len(movie_ids)
        ))
    print('Done!')
