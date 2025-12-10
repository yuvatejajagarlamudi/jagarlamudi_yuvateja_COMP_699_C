from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboards
    path("resident/dashboard/", views.resident_dashboard, name="resident_dashboard"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
