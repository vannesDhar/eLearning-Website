from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from eLearningApp.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path('ws/eLearningProj/home/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

