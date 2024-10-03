"""
ASGI config for rollin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from websocket import consumers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rollin.settings")




ws_patterns = [
    path("ticker", consumers.BTCTicker.as_asgi())
]

application = ProtocolTypeRouter({
      "http": get_asgi_application(),
    "websocket": URLRouter(ws_patterns)
})