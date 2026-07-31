"""
ASGI config for Autonomous Activation System project.
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "autonomous_activation_system.config.settings"
)

django_asgi_app = get_asgi_application()

from autonomous_activation_system.websocket.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})
