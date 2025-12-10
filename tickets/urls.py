from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("submit/", views.submit_issue, name="submit"),
    path("my-issues/", views.my_issues, name="my_issues"),
    path("list/", views.ticket_list, name="list"),
    path("view/<int:ticket_id>/", views.view_ticket, name="view"),
    path("assign/<int:ticket_id>/", views.assign_ticket, name="assign"),
    path("change-status/<int:ticket_id>/", views.change_status, name="change_status"),
    path("download-history/", views.download_history, name="download_history"),
]
