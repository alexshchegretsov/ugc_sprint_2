from sanic import Blueprint

from .event_views import event_view_bp

view_events = Blueprint.group(event_view_bp, url_prefix='/events')
