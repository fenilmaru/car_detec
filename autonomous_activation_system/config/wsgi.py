"""
WSGI config for Autonomous Activation System project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "autonomous_activation_system.config.settings"
)

application = get_wsgi_application()
