from sanic import Blueprint

from .bookmarks import bookmarks_bp
from .events import view_events
from .movie_marks import movie_marks_bp
from .reviews import movie_reviews_bp

ugc_api = Blueprint.group(view_events, movie_marks_bp, movie_reviews_bp, bookmarks_bp, url_prefix='/ugc')
