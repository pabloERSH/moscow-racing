from django.urls import re_path
from .consumers import RatingConsumer


ws_urlpatterns = [
    re_path(r'ws/socket-server/', RatingConsumer.as_asgi())
]
