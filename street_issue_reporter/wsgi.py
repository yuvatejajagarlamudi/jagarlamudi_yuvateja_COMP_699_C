"""
WSGI config for street_issue_reporter project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'street_issue_reporter.settings')

application = get_wsgi_application()
