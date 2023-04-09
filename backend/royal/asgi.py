"""
ASGI config for royal project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import channels_graphql_ws
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack, get_user
from django.urls import path 

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "royal.settings")

import django
django.setup()

from royal.schema import schema as schm

django_asgi_app = get_asgi_application()

class GraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    async def on_connect(self, payload):
        self.scope["user"] = await get_user(self.scope)

    schema = schm

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/", GraphqlWsConsumer.as_asgi()),
        ])
    ),
})
