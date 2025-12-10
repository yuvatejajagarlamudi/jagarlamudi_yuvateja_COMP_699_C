# street_issue_reporter/street_issue_reporter/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home Page
    path('', TemplateView.as_view(template_name="home.html"), name="home"),

    # Accounts App
    path('accounts/', include('accounts.urls')),

    # Tickets App
    path('tickets/', include('tickets.urls')),
]

# Serve media files (uploaded images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
