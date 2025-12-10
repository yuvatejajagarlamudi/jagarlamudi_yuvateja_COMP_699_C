"""
ASGI config for street_issue_reporter project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_issue_reporter.settings')

application = get_asgi_application()
