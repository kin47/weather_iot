from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'stream-video', consumers.VideoConsumer.as_asgi()),
]